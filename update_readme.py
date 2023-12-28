import os
from pathlib import Path

_BLOG_PATH: Path = Path.cwd()
_POSTS_PATH: Path = _BLOG_PATH / "posts"

_INTRO: str = """# Aiden's Blog 

I like to write about topics in mathematics, computer science, and quantitative finance. 

There is no set goal for this blog other than to help me jot down ideas or improve my understanding, 
and perhaps others may find my thoughts useful or interesting. 

The types of posts one can expect are: 
- A more detailed derivation/implementation of a well-known topic. 
- An exploratory analysis of an idea. 
- An explanation of a topic that I am more familiar with. 
- A comment/reaction to current events. 

## List of posts 

"""


with open(file=_BLOG_PATH / "README.md", mode="w") as readme:
    # print(type(readme)) # TextIOWrapper
    readme.write(_INTRO)
    for blog_post in os.listdir(_POSTS_PATH):
        if blog_post.startswith("."):
            continue
        print(str(_POSTS_PATH / blog_post / "README.md"))
        with open(file=_POSTS_PATH / blog_post / "README.md", mode="r") as blog_md:
            blog_code, blog_title = blog_md.readline().split(":")
            blog_code = blog_code.replace("# ", "")
            blog_title = blog_title.replace("\n", "").strip()
        readme.write(
            f"\n- [{blog_code}: {blog_title}](posts/{blog_post}/README.md) "
        )  # TODO: not sure about Path concatonation
