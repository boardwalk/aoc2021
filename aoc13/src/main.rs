use std::io::{self, BufRead};
use anyhow::{anyhow, Error};
use std::str::FromStr;
use std::collections::HashSet;

const PART2: bool = true;

#[derive(Debug, Clone, Copy)]
enum FoldInstruction {
    X(i32),
    Y(i32),
}

fn main() -> Result<(), Error> {
    let mut dots = HashSet::new();

    for line in io::stdin().lock().lines() {
        let line = line?;
        if line.is_empty() {
            break;
        }

        let mut tokens = line.split(",");

        let x_str = tokens.next().ok_or_else(|| anyhow!("missing token"))?;
        let y_str = tokens.next().ok_or_else(|| anyhow!("missing token"))?;

        let x = i32::from_str(x_str)?;
        let y = i32::from_str(y_str)?;

        dots.insert((x, y));
    }

    let mut folds = Vec::new();

    for line in io::stdin().lock().lines() {
        let line = line?;
        if line.is_empty() {
            break;
        }

        if line.starts_with("fold along x=") {
            let rest = &line["fold along x=".len()..];
            let x = i32::from_str(rest)?;
            folds.push(FoldInstruction::X(x));
        } else if line.starts_with("fold along y=") {
            let rest = &line["fold along y=".len()..];
            let y = i32::from_str(rest)?;
            folds.push(FoldInstruction::Y(y));
        } else {
            return Err(anyhow!("Invalid fold instruction"));
        }
    }

    println!("dots = {:?}", dots);
    println!("folds = {:?}", folds);

    for fold in folds.iter().copied() {
        let mut new_dots = HashSet::new();

        for (dot_x, dot_y) in dots.iter().copied() {
            let new_dot = match fold {
                FoldInstruction::X(fold_x) => {
                    if dot_x < fold_x {
                        (dot_x, dot_y)
                    } else if dot_x == fold_x {
                        return Err(anyhow!("Dot on x fold line"));
                    } else {
                        (2 * fold_x - dot_x, dot_y)
                    }
                }
                FoldInstruction::Y(fold_y) => {
                    if dot_y < fold_y {
                        (dot_x, dot_y)
                    } else if dot_y == fold_y {
                        return Err(anyhow!("Dot on yfold line"));
                    } else {
                        (dot_x, 2 * fold_y - dot_y)
                    }
                }
            };

            new_dots.insert(new_dot);
        }

        dots = new_dots;

        if !PART2 {
            break;
        }
    }

    let max_dot_x = dots.iter().copied().map(|(x, y)| x).max().ok_or_else(|| anyhow!("no dots!"))?;
    let max_dot_y = dots.iter().copied().map(|(x, y)| y).max().ok_or_else(|| anyhow!("no dots!"))?;

    println!("number of dots: {:?}", dots.len());
    println!("max dot x={:?} y={:?}", max_dot_x, max_dot_y);

    for y in 0..=max_dot_y {
        for x in 0..=max_dot_x {
            if dots.contains(&(x, y)) {
                print!("x");
            } else {
                print!(".");
            }
        }

        println!("");
    }

    Ok(())
}
