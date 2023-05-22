from antlr4 import *
from FJadeLexer import FJadeLexer
from FJadeParser import FJadeParser
from FJadeListener import FJadeListener
import argparse as ap
import os
from os import path
import asyncio

argparser = ap.ArgumentParser(description="A command-line tool for converting between FrozenJade code and DiamondFire Templates.")
subparsers = argparser.add_subparsers(dest="method", help="The method of conversion")

tparser = subparsers.add_parser("transpile", help="Tranpile FrozenJade code to DiamondFire Templates")
tparser.add_argument("input_file", help="Path to input file(s) (If a directory is provided, it will recursively transpile all files)")
tparser.add_argument("--output_file", help="Path to output (mode: w+)", default="stdout", required=False)
tparser.add_argument("--stdout", help="Also prints the output to stdout", action="store_true")
tparser.add_argument("--compress", help="Automatically compress the output (if using stdout then compresses it and print, or if output file is specifies then it will be a .b64 file)", action="store_true")
tparser.add_argument("--send", help="Sends the compressed transpiled code to a recode client", action="store_true")
tparser.add_argument("--prog-name", help="Program name that uses this tool. Default: FrozenJade", const="FrozenJade", nargs='?')

rparser = subparsers.add_parser("reverse", help="Reverses DiamondFire Templates into FrozenJade code")
rparser.add_argument("input_file", help="Input json / base64 file")
rparser.add_argument("output_file", help="Output FrozenJade file", default="stdout")
rparser.add_argument("--stdout", help="Als prints the output code to stdout", action="store_true")
rparser.add_argument("--style", help="The code style to generate (https://en.wikipedia.org/wiki/Indentation_style#Brace_placement_in_compound_statements)")
rparser.add_argument("--indent", type=int, help="The number of spaces to use for indentation")

argparser.add_argument("-o", help="Silent stdout output.", action="store_true")
args = argparser.parse_args()

async def transpile(path):
    input_stream = FileStream(path)
    lexer = FJadeLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = FJadeParser(stream)
    tree = parser.fjade()
    executer = FJadeListener()
    walker = ParseTreeWalker()
    walker.walk(executer, tree)

    if (args.stdout or args.output_file == "stdout") and not args.o:
        if args.compress:
            print(executer.template.compress())
        elif not args.compress:
            print(str(executer.template))
    if not args.output_file == "stdout":
        with open(args.output_file, "w+") as output_file:
            if args.compress:
                output_file.write(executer.template.compress())
            elif not args.compress:
                output_file.write(str(executer.template))
    if args.send:
        await executer.template.send(f"&e&l{executer.template.blocks[0].category.upper()} &f> &a&o \
{executer.template.blocks[0].action if executer.template.blocks[0].action else executer.template.blocks[0].extra['data']}".replace("&", "§"),
                                     args.prog_name if args.prog_name else "FrozenJade")

if args.method == "transpile":
    if path.isdir(args.input_file):
        async def visit(dir):
            for f in os.listdir(dir):
                if path.isdir(f):
                    await visit(f"{dir}/{f}/")
                else:
                    await transpile(f"{dir}/{f}")
        asyncio.run(visit(args.input_file))
    else:
        asyncio.run(transpile(args.input_file))

