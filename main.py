import subprocess
import os

local_dir = os.path.dirname(os.path.realpath(__file__))

def validate_post_id(post_id: str) -> bool:
    result = subprocess.run(["ls", local_dir + "/markdown"], capture_output=True, text=True)
    file_names = [s.strip() for s in result.stdout.split("\n")]
    return (post_id + ".md") in file_names

def add_post(post_id: str):
    markdown_file_path = f"{local_dir}/markdown/{post_id}.md"

    # Manually ensure that the min-width is 50% of the page
    styling_text = "```{=html}\n<style>\nbody { min-width: 50% !important; }\n</style>\n```\n"
    # Also add back link
    back_link_text = "<center align='center'><a href='../index.html'>Back</a></center>\n"
    with open(markdown_file_path, "r") as file:
        original_text = file.read()
        new_text = styling_text + original_text
        new_text = back_link_text + new_text
    with open(markdown_file_path, "w") as file:
        file.write(new_text)

    subprocess.run(
        f"cd {local_dir} && pandoc -o posts/{post_id}.html -s --highlight-style my.theme {markdown_file_path}", 
        stdout=subprocess.DEVNULL,
        shell=True,
    )

    with open(markdown_file_path, "w") as file:
        file.write(original_text)

def get_valid_post_id(prompt: str) -> str:  
    post_id = input(prompt)
    valid = validate_post_id(post_id)
    if not valid:
        print("Invalid post id")
        return get_valid_post_id(prompt)
    else: 
        return post_id

def handle_add():
    post_id = get_valid_post_id("Id of the post you would like to add:\n")
    add_post(post_id)

def handle_delete():
    post_id = get_valid_post_id("Id of the post you would like to delete:\n")
    add_post(post_id)

def handle_refresh():
    post_id = get_valid_post_id("Id of the post you would like to refresh (input 'all' to refresh all posts):\n")
    add_post(post_id)


def run():
    command = input("What would you like to do? Options: add, delete, refresh\n")
    match command.strip():
        case "add":
            handle_add()
        case "delete":
            handle_delete()
            pass
        case "refresh":
            handle_refresh()
            pass
        case _:
            print("Invalid input")
            run()

run()