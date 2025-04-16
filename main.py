import os
import pysubs2
import random
from time import sleep
from tqdm_joblib import tqdm_joblib
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from pathlib import Path
from joblib import Parallel, delayed
from openai import OpenAI

EXTRACT_PROMPT = """
Above is the transcript of a lecture. Follow the instructions below.

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

# Formatting

Report each occurrence with controlled bolding and italicizing. Format your response in exactly the following pattern:

### 1. Title
**Key Points**
- [Important or emphasized key points as bullet list]

(If there's an example:) **Problem statement:**
[Example problem]

(If there's an example:) **Solution:**
[Professor's solution and line of thinking]

_Summary of this item, any additional information, things you would like to add based on information given in the transcript._

""".strip()

GEN_EXAM_PROMPT = f"""
You will be given lecture analysis documents and you will need to synthesize an exam based on the details extracted from the lecture recordings.

Here is an example of an exam (do not copy the questions from here):
{Path("./exam1.md").read_text(encoding="utf-8")}

Focus on writing design oriented questions like in the style of the above exam. Give us example scenarios and then ask us design questions about it. The questions must be somehow novel, not directly taken from the practice material or lecture notes. They need to be questions that force the students to reason about the material and think beyond what the lecture has given them considering tradeoffs. 

# Formatting

Provide each exam-style question in exactly the following format:

### Question 1
[Any conditions, setup, etc. of the question]

[Content of the question itself, and/or any followup/sub-questions.]

""".strip()

def get_parser():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--subtitles",
        help="path to subtitles",
        default="./subtitles",
        type=str,
    )
    parser.add_argument(
        "--gems",
        help="gems directory path",
        default="./gems",
        type=str,
    )
    parser.add_argument(
        "--model",
        help="OpenAI model ID",
        default="o3-mini",
        type=str,
    )
    parser.add_argument(
        "--extract", help="extract vital info from transcripts", action="store_true"
    )
    parser.add_argument(
        "--exam_gen", help="generate exam-style questions", action="store_true"
    )
    parser.add_argument(
        "--fake",
        help="prevent actual extraction (--extract) from happening for progressbar testing.",
        action="store_true"
    )
    return parser


def run(file):
    client = OpenAI()
    subs = pysubs2.load(file, encoding="utf-8")
    text = "\n".join(line.text for line in subs)
    response = client.responses.create(
        input=text,
        model=args.model,
        instructions=EXTRACT_PROMPT,
    )
    with open(Path(args.gems) / (file.stem + ".md"), "w", encoding="utf-8") as f:
        f.write(response.output_text)


def main(args):
    if args.extract:
        with tqdm_joblib(
            desc="Extraction progress",
            total=len(list(Path(args.subtitles).iterdir())),
            unit='vid',
            dynamic_ncols=True,
            colour=f'#{random.randint(0, 16777215):06x}'
        ) as _:
            if args.fake:
                Parallel(n_jobs=os.cpu_count())(delayed(sleep)(i) for i in range(15))
            else:
                Parallel(n_jobs=os.cpu_count())(
                    delayed(run)(file) for file in Path(args.subtitles).iterdir()
                )
    elif args.exam_gen:
        client = OpenAI()
        prompt = ""
        for file in Path(args.gems).glob("*.md"):
            prompt += f"# {file.stem}:\n\n{file.read_text(encoding='utf-8')}\n\n"
        response = client.responses.create(
            input=prompt,
            model=args.model,
            instructions=GEN_EXAM_PROMPT,
        )
        Path("exam2.md").write_text(response.output_text, encoding='utf-8')
    else:
        parser.print_help()


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args)
