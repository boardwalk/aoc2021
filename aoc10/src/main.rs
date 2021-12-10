use anyhow::{bail, Result};
use std::io::{self, BufRead};

const PART2: bool = true;

struct Grouper {
    open: u8,
    close: u8,
    inc_score: u64,
    bad_score: u64,
}

const GROUPERS: [Grouper; 4] = [
    Grouper { open: b'(', close: b')', inc_score: 1u64, bad_score: 3u64 },
    Grouper { open: b'[', close: b']', inc_score: 2u64, bad_score: 57u64 },
    Grouper { open: b'{', close: b'}', inc_score: 3u64, bad_score: 1197u64 },
    Grouper { open: b'<', close: b'>', inc_score: 4u64, bad_score: 25137u64 },
];

fn eval_line(line: io::Result<Vec<u8>>) -> Result<u64> {
    let mut grouper_stack = Vec::new();
    let mut bad_score = 0;
    for ch in line?.into_iter() {
        if let Some(grouper) = GROUPERS.iter().find(|grouper| grouper.open == ch) {
            grouper_stack.push(grouper);
        } else if let Some(grouper) = GROUPERS.iter().find(|grouper| grouper.close == ch) {
            if grouper_stack.last().map(|grouper| grouper.open) == Some(grouper.open) {
                grouper_stack.pop();
            } else {
                bad_score = grouper.bad_score;
                break;
            }
        } else {
            bail!("unknown character {}", ch);
        }
    };

    let line_score = if PART2 {
        if bad_score == 0 {
            // Process partial/complete line
            grouper_stack.iter().fold(0, |accum, grouper| accum * 5 + grouper.inc_score)
        } else {
            // Discard broken line
            0
        }
    } else {
        bad_score
    };

    Ok(line_score)
}

fn main() -> Result<()> {
    let mut scores = io::stdin().lock().split(b'\n').map(eval_line).collect::<Result<Vec<u64>>>()?;
    scores.retain(|&score| score != 0);

    let final_score = if PART2 {
        if scores.len() % 2 != 1 {
            bail!("not an odd amount of scores");
        }

        scores.sort();
        scores[scores.len() / 2]
    } else {
        scores.iter().fold(0, |accum, item| accum + item)
    };

    println!("final score is {}", final_score);
    Ok(())
}
