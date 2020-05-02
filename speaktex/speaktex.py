import pathlib

from tex2py import tex2py

def speaktex(tex_filename: pathlib.Path):
    with tex_filename.open('r') as tex_file:
        data = tex_file.read()
    tex_tree = tex2py(data)
    print(tex_tree)
