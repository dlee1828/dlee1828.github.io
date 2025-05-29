# Overview of C/C++ Macros

The following are some examples of macros in C/C++:

```cpp
// A basic macro:
#define PI 3.14

/*
A function-like macro:

We use parentheses around the arguments to avoid order-of-operations
issues.

For example, consider what would happen if we didn't have the parentheses
and we called MULTIPLY(1 + 1, 2)
*/
#define MULTIPLY(x, y) (x) * (y)

/* 
A multi-line macro:

We wrap the logic in a do-while statement to ensure that the macro can 
be used in the body of an if statement without braces:
	if (condition) SWAP(x, y);
	else doSomethingElse();
*/
#define SWAP(x, y) do { \
    typeof(x) temp = x; \
    x = y; \
    y = temp; \
} while (0)

// We can use "#" to convert a macro argument into a string
#define PRINT(x) std::cout << #x << " = " << x << std::endl;

/* 
We can use "##" to concatenate two tokens into one token

__LINE__ is a predefined macro which expands to the line number at
which it is written. Other predefined macros include __FILE__
and __FUNCTION__. 
*/
#define GENERATE_UNIQUE(var) var##__LINE__

int GENERATE_UNIQUE(counter) = 0;

/*
We can also define variadic macros
The list of arguments is accessed through __VA_ARGS__
*/
#define PRINT(...) printf(__VA_ARGS__)

int main() {
    PRINT("Hello %s", "world");
    return 0;
}
```

The use of macros is generally discouraged in C and C++ because they’re difficult to debug, can have strange side effects if you’re not careful, and pollute the global scope. Moreover, most of the things you’d want to accomplish through object-like or function-like macros can be done more safely using `const` variables and `inline` functions (`const` and `inline` didn’t exist in the early days of C, so macros were the only way to define constants or achieve inlined functions). 

Despite their downsides, some people argue that macros can be useful for code generation in situations where you need to write a lot of similar definitions or statements. 

In addition, something you can only do with macros is convert code into strings.  For example, it would not be possible to implement an assert function like this without a macro:

```cpp
#define ASSERT(expr) (expr) ? 0 : printf("Assertion failed: %s\n", #expr) 
```

Macros are also necessary to utilize predefined macros effectively.  For example, suppose you want to write a function which, when called, prints the line number of the line at which it is invoked. It’s easy to see how something like this could be useful for debugging. We already know that we can access the current line number through the predefined `__LINE__` macro. So you might think that something like this would work:

```cpp
inline void PRINT_LINE() {
    std::cout << "line: " << __LINE__ << std::endl;
}

int main() {
    PRINT_LINE();
    return 0;
}
```

However, this actually doesn’t work because the `__LINE__` macro is expanded at the point at which it is written in the code. So whenever you call `PRINT_LINE`, the function will always print the line at which `__LINE__` exists in the function definition. 

So in order for this to work, we have to use a macro:

```cpp
#define PRINT_LINE() std::cout << "line: " << __LINE__ << std::endl;

int main() {
    PRINT_LINE();
    return 0;
}
```

`PRINT_LINE` now works the way we want it to.