import os
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from pathlib import Path

import pysubs2
from joblib import Parallel, delayed
from openai import OpenAI


def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--subtitles",
        help="path to subtitles",
        default="subtitles",
        type=str,
    )
    parser.add_argument(
        "--gems",
        help="gems directory path",
        default="gems",
        type=str,
    )
    parser.add_argument(
        "--model",
        help="extraction model id",
        default="o3-mini",
        type=str,
    )
    parser.add_argument("--extract", help="extract", action="store_true")
    parser.add_argument("--exam_gen", help="generate exam", action="store_true")
    return parser.parse_args()


EXTRACT_PROMPT = """
# Instructions from Professor

Review my lecture recordings, religiously. And please listen very actively and take notes. I structure lectures in such a way that an attentive listener will extract enough questions and hints about exam interlaced with the delivery of the main content.
1. e.g. for each such example covered in lecture, please make sure you can solve this example yourself. Copy the problem into your response, as well as my solution
2. Especially make sure to note down situations I do the following:
    - I frequently say things like : "if I were to ask you this on the exam". Make sure to include these
    - I often emphasize specific things as being very important or fundamental
    - I introduce concrete examples (like we did in the Atomicity 1 lecture, or the VMM lecture, considering 1-level page tables,  etc)
3. Try to follow my line of thinking: how I conceptualize thing, how I give knowledge structure. I assert that everything can be derived from first principles.

# Your Task

Your task is to analyze the user's lecture transcript and find all these examples that could be possibly on the exam, according to the Professor's hints. Output a detailed list of wherever these examples occur in the lecture.
""".strip()

GEN_EXAM_PROMPT = f"""
You will be given lecture analysis documents and you will need to synthesize an exam based on the details extracted from the lecture recordings.

Here is an example of an exam (do not copy the questions from here):
{Path("./exam1.md").read_text()}
"""


def run(file):
    client = OpenAI()
    subs = pysubs2.load(file, encoding="utf-8")
    text = "\n".join(line.text for line in subs)
    response = client.responses.create(
        input=text,
        model=args.model,
        instructions=EXTRACT_PROMPT,
    )
    with open(Path(args.gems) / (file.stem + ".md"), "w") as f:
        f.write(response.output_text)


def main(args):
    if args.extract:
        Parallel(n_jobs=os.cpu_count())(
            delayed(run)(file) for file in Path(args.subtitles).iterdir()
        )

    if args.exam_gen:
        client = OpenAI()
        prompt = ""
        for file in Path("./gems").glob("*.md"):
            prompt += f"# {file.stem}:\n\n{file.read_text()}\n\n"
        response = client.responses.create(
            input=prompt,
            model=args.model,
            instructions=GEN_EXAM_PROMPT,
        )
        Path("exam2.md").write_text(response.output_text)


if __name__ == "__main__":
    args = parse_args()
    main(args)
