# Adding a Feature to GNU Make

## Motivation

GNU Make is a neat tool. However, there are some aspects of it which occasionally receive criticism. One of these is the way phony targets are specified. 

Make reads from a set of rules written in a Makefile. Most of these rules are used to build files, but it’s also common to have rules which just run a series of commands (`make clean`, `make install`, etc). It’s important to indicate to Make that such rules don’t correspond to actual files, as otherwise, Make may skip running the commands. For example, if you happen to have a file named `install` in your project directory, and then you run `make install`, Make won’t actually run your install commands and you’ll receive the following message: 

```
make: 'install' is up to date.
```

This happens because Make thinks that your rule is attempting to build a file called `install`, and it notices that this file already exists. 

The solution is to declare certain targets phony, indicating that they don’t correspond to actual files. We do this by listing all phony targets as dependencies of a built-in target called `.PHONY`.

```makefile
.PHONY: clean install

clean:
	@echo "Cleaning..."
	
install:
	@echo "Installing..."
```

But this syntax is a bit awkward. To quote from the README of [just](https://github.com/casey/just),

> …the syntax is verbose and can be hard to remember. The explicit list of phony targets, written separately from the recipe definitions, also introduces the risk of accidentally defining a new non-phony target.
> 

A simple way to improve this syntax would be to allow users to specify phony targets directly in their rules.
Consider, for example, if you could indicate that a target is phony by prefixing its name with an underscore:

```makefile
_clean:
	@echo "Cleaning..."

_install:
	@echo "Installing..."
```

The user could then run `make clean` or `make install` as usual, and `clean` and `install` would be treated as phony targets. 

I decided to try adding this feature to Make.

## Setting up 

I chose to work with version 4.3 of Make, released in 2020. 
After building Make inside an Ubuntu Docker container, I ran the provided tests and noticed that one test failed:

```
misc/fopen-fail ......................................... 
Error running make (expected 512; got 11): 'make' '-f' 'work/misc/fopen-fail.mk'

Caught signal 11!
FAILED (0/1 passed)
```

After some digging, I learned that the reason the test failed was because Docker prevents programs from setting system-wide limits through `ulimit` (see [here](https://stackoverflow.com/a/24331638)). The `fopen-fail` test attempts to use `ulimit -n 512` to limit the maximum number of open file descriptors. But Docker prevents this from happening, which results in a segmentation fault when the test runs. So I manually ran `ulimit -n 512` prior to running the test, and that got it to pass.

## Gathering information

After sifting through the code for a bit, I was able to gather the following facts:

1. Information about targets and dependencies gets stored in a struct called `file`:

```c
struct file
  {
    const char *name;
    const char *hname;          /* Hashed filename */
    const char *vpath;          /* VPATH/vpath pathname */
    struct dep *deps;           /* all dependencies, including duplicates */
    struct commands *cmds;      /* Commands to execute for this target.  */
 
	  /* Many more members I'm skipping over... */ 
 
    unsigned int is_target:1;   /* Nonzero if file is described as target.  */
    unsigned int cmd_target:1;  /* Nonzero if file was given on cmd line.  */
    unsigned int phony:1;       /* Nonzero if this is a phony file
                                   i.e., a prerequisite of .PHONY.  */
    /* More members... */
  };

```

Notice that one of these members indicates whether the file is phony.

2. The structs corresponding to all the targets and dependencies present in the Makefile get stored in a hash table called `files`: 

```c
static struct hash_table files;
```

3. There is a function called `read_all_makefiles` which gets called in `main`. `read_all_makefiles` eventually calls `enter_file`, a function which is used to add and retrieve entries from the `files` hash table. 
When Make reads a Makefile, `enter_file` is called with the name of each target. 
    
## Writing code

It seemed like I could implement my feature by doing the following: in `enter_file`, detect if the name of the target begins with an underscore. If it does, modify the target’s associated `file` struct to indicate that it is phony. 

I wrote this function which mimics what is done elsewhere in the code to establish that a particular file is a phony target:

```c
void make_file_phony (struct file* f) {
  f->phony = 1;
  f->is_target = 1;
  f->last_mtime = NONEXISTENT_MTIME;
  f->mtime_before_update = NONEXISTENT_MTIME;
}
```

I set `phony` and `target` to 1 and set variables storing modification times to values indicating that the file does not exist. 

I then used this function in the body of `enter_file` as such:

(⬅️ indicates a line I added)

```c
struct file *
enter_file (const char *name)
{
  struct file *f;
  struct file *new;
  struct file **file_slot;
  struct file file_key;

  assert (*name != '\0');
  assert (! verify_flag || strcache_iscached (name));

  int underscored = name[0] == '_'; // ⬅️
  if (underscored) {                // ⬅️
    name = name + 1;                // ⬅️
  }                                 // ⬅️

  // (VMS-specific code omitted for brevity)

  file_key.hname = name;
  file_slot = (struct file **) hash_find_slot (&files, &file_key);
  f = *file_slot;
  if (! HASH_VACANT (f) && !f->double_colon)
    {
      f->builtin = 0;
      if (underscored) make_file_phony(f); // ⬅️
      return f;
    }

  new = xcalloc (sizeof (struct file));
  new->name = new->hname = name;
  new->update_status = us_none;
  if (underscored) make_file_phony(new); // ⬅️

  if (HASH_VACANT (f))
    {
      new->last = new;
      hash_insert_at (&files, new, file_slot);
    }
  else
    {
      /* There is already a double-colon entry for this file.  */
      new->double_colon = f;
      f->last->prev = new;
      f->last = new;
    }

  return new;
}
```

## Discussion

There are two details worth discussing. The first concerns the following code:

```c
 if (underscored) {
    name = name + 1;
  }   
```

If I detect that a name begins with an underscore, I remove the underscore from the name. I do this because aside from in its own rule, I don’t want the user to have to use an underscore every time they reference a phony target. For example, if the user wants to list a phony target as a dependency, they should be able to do so without the underscore:

```makefile
_this_is_phony: 
	@echo "hi"
	
another_target: this_is_phony
	@echo "hi"
```

Moreover, a user should be able to run this recipe using `make this_is_phony`, without needing the underscore. 

So I remove the underscore in `enter_file` to ensure that the target is stored internally with its non-underscored name. 

Also, I call `make_file_phony` both when creating a new file entry in the hash table *and* when retrieving an existing entry. This may seem unnecessary - shouldn’t we only need to set the file to phony when its entry is first created? This is what I thought initially. However, I realized that calling `make_file_phony` in both cases is necessary because of what I described above: a phony target can be referenced without an underscore. And it is possible for `enter_file` to get called with a phony target’s non-underscored name prior to getting called with its underscored name. If this happens, an entry for the target will get created in the hash table without that entry being marked phony. And if we only set underscored files to phony upon creation, then our target will not get marked phony, even when its rule is encountered and `enter_file` gets called with its underscored name. 

## Testing

After making these changes, I tested the new feature with the following Makefile:

```makefile
# Phony target
_abc:
	@echo "abc: This target should be phony. \
	This recipe should run even if there is a file \
	named abc or _abc in the directory."

# Non-phony target
def:
	@echo "def: This target is not phony. \
	This recipe should not run if there is a \
	file named def in the directory."

# Non-phony target dependent on phony target
ghi: abc
	@echo "ghi: This target depends on abc. \
	This message and abc's message should get printed \
	even if there exists a file named ghi in the directory."

# Phony target dependent on up-to-date non-phony target
_jkl: def
	@echo "jkl: This should be a phony target. \
	It depends on non-phony target def. \
	def's message should not be printed if there is a file \
	named def in the directory."
```

I also re-ran the source code’s original tests and verified that they all still pass (as long as I manually run `ulimit -n 512`).