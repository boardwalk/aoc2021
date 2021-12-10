use std::io;

const PART2: bool = true;

fn make_err(msg: String) -> io::Result<()> {
    Err(io::Error::new(io::ErrorKind::Other, msg))
}

fn main() -> io::Result<()> {
    let mut line = String::new();
    let mut grouper_stack = Vec::new();
    let mut scores = Vec::new();

    loop {
        io::stdin().read_line(&mut line)?;

        if line.is_empty() {
            break;
        }

        let mut line_score = 0u64;
        let mut broken = false;

        for ch in line.trim_end().chars() {
            let score = match ch {
                '(' | '[' | '{' | '<' => {
                    grouper_stack.push(ch);
                    None
                }
                ')' => {
                    if grouper_stack.pop() != Some('(') {
                        Some(3u64)
                    } else {
                        None
                    }
                }
                ']' => {
                    if grouper_stack.pop() != Some('[') {
                        Some(57u64)
                    } else {
                        None
                    }
                }
                '}' => {
                    if grouper_stack.pop() != Some('{') {
                        Some(1197u64)
                    } else {
                        None
                    }
                }
                '>' => {
                    if grouper_stack.pop() != Some('<') {
                        Some(25137u64)
                    } else {
                        None
                    }
                }
                _ => {
                    return make_err(format!("unknown character {}", ch));
                }
            };

            if let Some(score) = score {
                if !PART2 {
                    line_score += score;
                }

                broken = true;
                break;
            }
        }

        if !broken && PART2 {
            while let Some(ch) = grouper_stack.pop() {
                let score = match ch {
                    '(' => 1u64,
                    '[' => 2u64,
                    '{' => 3u64,
                    '<' => 4u64,
                    _ => {
                        panic!("logic error");
                    }
                };

                line_score = line_score * 5 + score;
            }
        }

        if line_score != 0 {
            scores.push(line_score);
        }

        line.clear();
        grouper_stack.clear();
    }

    let total_score = if PART2 {
        if scores.len() % 2 != 1 {
            return make_err(format!("not an odd amount of scores"));
        }

        scores.sort();
        scores[scores.len() / 2]
    } else {
        scores.iter().copied().reduce(|x, y| x + y).unwrap_or(0)
    };

    println!("score is {}", total_score);
    Ok(())
}
