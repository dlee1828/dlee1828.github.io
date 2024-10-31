To add a new blog post:
1. Create a new markdown file in `/markdown`
2. Write the blog post in that file
3. Add the id and title of the post to `posts-info.json`. 
   The id of the post is the name of the markdown file, excluding the file extension.
   The title of the post is whatever you want the title of the post to be.
4. Run `python3 refresh.py`.