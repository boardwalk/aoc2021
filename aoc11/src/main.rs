use std::io;
use std::collections::HashSet;
use anyhow::{anyhow, bail, Result};

const PART2: bool = true;

struct Cavern {
    octopuses: Vec<u8>,
    width: i8,
    height: i8,
}

impl Cavern {
    fn from_reader<R: io::BufRead>(reader: R) -> Result<Self> {
        let mut octopuses = Vec::new();
        let mut opt_width = None;
        let mut height = 0i8;

        for line in reader.split(b'\n') {
            let line = line?;
            let this_width = i8::try_from(line.len())?;

            if let Some(width) = opt_width {
                if this_width != width {
                    bail!("Expected line width {}, found {} on line {}", width, this_width, height);
                }
            } else {
                opt_width = Some(this_width);
            }

            const ZERO: u8 = 48;
            const NINE: u8 = ZERO + 9;

            for b in line.into_iter() {
                if b >= ZERO && b <= NINE {
                    octopuses.push(b - ZERO);
                }  else {
                    bail!("Input is not a digit");
                }
            }

            height += 1;
        }

        let cavern = Self {
            octopuses,
            width: opt_width.ok_or_else(|| anyhow!("No lines found"))?,
            height,
        };

        Ok(cavern)
    }

    fn get(&self, x: i8, y: i8) -> u8 {
        if x >= 0 && x < self.width && y >= 0 && y < self.height {
            let idx = x as usize + y as usize * self.width as usize;
            self.octopuses[idx]
        } else {
            0
        }
    }

    fn set(&mut self, x: i8, y: i8, e: u8) {
        if x >= 0 && x < self.width && y >= 0 && y < self.height {
            let idx = x as usize + y as usize * self.width as usize;
            self.octopuses[idx] = e;
        }
    }

    fn len(&self) -> usize {
        self.octopuses.len()
    }

    fn step(&mut self) -> usize {
        let mut flash_stack = Vec::new();

        for x in 0..self.width {
            for y in 0..self.height {
                let energy = self.get(x, y).saturating_add(1);
                self.set(x, y, energy);
                if energy > 9 {
                    flash_stack.push((x, y));
                }
            }
        }

        let mut flashed = HashSet::new();
        while let Some((x, y)) = flash_stack.pop() {
            if flashed.contains(&(x, y)) {
                continue;
            }

            for dx in -1i8..=1 {
                for dy in -1i8..=1 {
                    if dx == 0 && dy == 0 {
                        continue;
                    }
                    let energy = self.get(x + dx, y + dy).saturating_add(1);
                    self.set(x + dx, y + dy, energy);
                    if energy > 9 {
                        flash_stack.push((x + dx, y + dy));
                    }
                }
            }

            flashed.insert((x, y));
        }

        for &(x, y) in &flashed {
            self.set(x, y, 0);
        }

        flashed.len()
    }
}

fn main() -> Result<()> {
    let mut cavern = Cavern::from_reader(io::stdin().lock())?;

    if PART2 {
        let mut step_num = 0;

        loop {
            let flashes = cavern.step();
            step_num += 1;

            if flashes == cavern.len() {
                break;
            }
        }

        println!("all flashes on step {}", step_num);
    } else {
        let mut total_flashes = 0;

        for _i in 0..100 {
            let flashes = cavern.step();
            total_flashes += flashes;
        }

        println!("num flashes = {}", total_flashes);
    }

    Ok(())
}
