# Calibration from the accepted GPU article

Use these examples to understand this user's technical narrative voice when that voice is requested. A new supplied reference takes priority. Other authors and genres need their own fingerprint.

## The reference's habits

Long explanations carry several connected clauses, then an occasional short reaction changes the rhythm. The narrator owns decisions and mistakes. Physical verbs explain abstract work: stretch, squash, park, shuffle. Definitions can sit in footnotes so the main explanation keeps moving.

Humour attaches to a specific outcome and usually targets the author's own confidence. A failed optimization, an improvement that disappears when rounded, or a spreadsheet claiming knowledge it never measured supplies the material. The explanation still needs to work if the aside disappears.

Original reference:

> My first attempt was to calculate `hidden` once, park it in a GPU buffer, and let all 32 groups read it from there.

This gives the action to the narrator, names the objects, and uses a physical verb. Preserve that agency when describing later experiments.

Accepted continuation:

> I already had a kernel for small row counts, so after comparing the two I set a cutoff at 96 rows: anything below that uses the short-row path, and anything from 96 up gets the bigger tiles. I also checked the outputs at 95, 96, and 97. I know who wrote the condition and would prefer to catch his mistakes here.

The first sentence explains the decision; the next gives concrete verification; the last makes the narrator the target of the joke. This pattern works because those details belong to this experiment. Repeating the pattern mechanically would flatten the voice.

Another accepted passage:

> The paired projection went from 4.62 milliseconds to 13.35, almost 3 times slower. The down projection went from 3.72 to 5.90. I had successfully reduced the amount of waiting, at least in the shader, and considerably increased the amount of waiting for me, yipee.

Here the humour follows the measurements and depends on what “waiting” means to the GPU and to its author. Preserve the mechanism; don't transplant the line or its spelling to unrelated writing.

## The correction that mattered

The user identified “Across the measured shapes” as a remaining tell. Restoring “Across the shapes I tested” put the person back in the experiment. An audit must check agency as well as grammatical passive voice.

An earlier pass had chased small-word frequencies and sanded away this directness. The accepted pass restored I tested, I staged, I timed, and I made those comparisons wherever the source supported them.

## What the numbers taught us

In this article, the reference's mean sentence length was 22.28 words, with a standard deviation of 10.51. The original continuation was 16.31 with a standard deviation of 6.84; the accepted version was 22.63 with a standard deviation of 10.84. Restoring longer explanations and variation helped more than adding isolated punchy lines.

A paragraph-level classifier using 15 style features dropped from 71.1% balanced accuracy to 52.1%, near its 50% chance level. Some lexical and punctuation differences remained. Those results guided the revision; the user's reading determined whether it sounded right. These numbers describe this sample and aren't targets for other writing.

For this user, also honour explicit rules: contractions, digits, short paragraphs, no em dashes, and no rhetorical negation followed by a corrected framing. The reference itself may have longer paragraphs; apply the user's latest instructions to resolve that tension.
