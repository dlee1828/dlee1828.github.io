import subprocess
import os
import json

local_dir = os.path.dirname(os.path.realpath(__file__))

def validate_post_id(post_id: str) -> bool:
    result = subprocess.run(["ls", local_dir + "/markdown"], capture_output=True, text=True)
    file_names = [s.strip() for s in result.stdout.split("\n")]
    return (post_id + ".md") in file_names

def add_post(post_id: str, post_title: str):
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
        f"pandoc -o posts/{post_id}.html -s --highlight-style my.theme {markdown_file_path}", 
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        cwd=local_dir,
        shell=True,
    )

    # Need to add link to post in index.html
    index_file_path = f"{local_dir}/index.html"
    with open(index_file_path, "r") as file:
        contents = file.read()
        lines = contents.splitlines(keepends=True)
        link_html = f"<a href='posts/{post_id}.html'>{post_title}</a>"
        if link_html not in contents:
            target_line_num = -1
            for i, line in enumerate(lines):
                if "LINKS TO POSTS WILL GET GENERATED BELOW THIS LINE" in line:
                    target_line_num = i + 1
                    break
            if target_line_num == -1:
                raise Exception("Did not find placeholder comment in index.html")
            lines.insert(target_line_num, "\t" + link_html + "\n")

    with open(index_file_path, "w") as file:
        file.writelines(lines)

    with open(markdown_file_path, "w") as file:
        file.write(original_text)

def run():
    with open(f"{local_dir}/posts-info.json") as file:
        # Delete index.html
        subprocess.run("rm index.html && cp index-template.html index.html", cwd=local_dir, shell=True)

        posts_info_json = json.load(file)
        posts = posts_info_json["posts"]
        posts = reversed(posts) # Reverse so that posts appear in the correct order after being added
        for post in posts:
            id = post["id"]
            title = post["title"]
            if not validate_post_id(id):
                print(f"{id} is not a valid post id")
                return
            add_post(id, title)

run()

