# Hidden Markov Models — guessing fish species

The forward algorithm, Viterbi and Baum–Welch written from the recurrences,
then used to classify fish from their movement patterns in the KTH Fishing
Derby.

Assignment 2 of **DD2380 Artificial Intelligence**, KTH, autumn 2021.

📄 [Assignment brief](docs/Assignment_HMM_HT2021_P1.pdf) ·
[lecture on HMMs](docs/AI%20-%20HMMs.pdf) ·
[lecture on probabilistic reasoning](docs/AI%20-%20Probabilistic%20Reasoning.pdf)

## Part 1 — [the algorithms](HMM_0-3)

Standalone implementations, each reading a matrix problem on stdin and printing
the answer — the format the course's automatic grader expects.

| | what it does |
|---|---|
| [HMM0.py](HMM_0-3/HMM0.py) | next-step emission distribution: one multiplication through `A` then `B` |
| [HMM1.py](HMM_0-3/HMM1.py) | **forward algorithm** — probability of an observation sequence |
| [HMM2.py](HMM_0-3/HMM2.py) | **Viterbi** — the most likely hidden state sequence, with backpointers |
| [HMM3.py](HMM_0-3/HMM3.py) | **Baum–Welch** — estimating `A`, `B` and `π` from observations alone |
| [HMM3_question_9.py](HMM_0-3/HMM3_question_9.py) | Baum–Welch under different initialisations |
| [HMM3_question_10.py](HMM_0-3/HMM3_question_10.py) | the same, varying the model size |

Everything is plain Python — no numpy — so the recurrences are visible rather
than hidden behind matrix calls. Forward probabilities are rescaled at each
step, without which they underflow to zero on sequences of any length.

Test inputs and expected answers are in [`samples/`](samples).

## Part 2 — [playing the game](player.py)

Seventy fish of seven species swim past. Each emits one of eight observable
movements per step, and every species moves according to its own HMM. Guess a
fish's species; you are told immediately whether you were right, and what it
actually was.

The strategy:

1. **Wait and watch.** No guess is made for the first 110 steps — one HMM
   trained on a handful of observations tells you nothing, and a wrong guess is
   only useful for the correction it triggers.
2. **Classify by likelihood.** Each species has a model; run the forward
   algorithm for the target fish's observation sequence against all seven and
   take the highest.
3. **Learn only from mistakes.** `reveal` runs Baum–Welch **only when the guess
   was wrong**, re-estimating the model of the species it actually was, using
   that fish's observations. Correct guesses change nothing.

The models start as a single state with a random emission distribution over the
eight movements, perturbed slightly from uniform — identical rows would leave
Baum–Welch with no gradient to work with.

## Running

```bash
pip install -r requirements.txt      # requirements_win.txt on Windows
python main.py                        # the game
echo "..." | python HMM_0-3/HMM1.py   # the standalone algorithms
```
