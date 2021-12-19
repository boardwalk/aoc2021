#![allow(dead_code)]
#![allow(unused_variables)]

use anyhow::{anyhow, Error};
use lazy_static::lazy_static;
use regex::Regex;
use std::io::{stdin, BufRead};
use std::ops::{Add, Sub};
use std::str::FromStr as _;

#[derive(Clone, Copy, Debug, PartialOrd, PartialEq, Eq, Ord)]
struct Beacon {
    x: i32,
    y: i32,
    z: i32,
}

#[derive(Clone, Copy, Debug)]
struct Offset {
    x: i32,
    y: i32,
    z: i32,
}

impl Beacon {
    fn from_reader<R: BufRead>(mut reader: R) -> Result<Option<Self>, Error> {
        lazy_static! {
            static ref RE: Regex = Regex::new(r"(-?\d+),(-?\d+),(-?\d+)$").unwrap();
        }

        let mut line = String::new();
        reader.read_line(&mut line)?;

        let line_trim = line.trim_end();
        if line_trim.is_empty() {
            return Ok(None);
        }

        let captures = RE.captures(line_trim).ok_or_else(|| anyhow!("Failed to match Beacon line"))?;

        let x_str = captures.get(1).unwrap().as_str();
        let y_str = captures.get(2).unwrap().as_str();
        let z_str = captures.get(3).unwrap().as_str();

        let x = i32::from_str(x_str).unwrap();
        let y = i32::from_str(y_str).unwrap();
        let z = i32::from_str(z_str).unwrap();

        Ok(Some(Beacon { x, y, z }))
    }
}

impl Add<Offset> for Beacon {
    type Output = Self;
    fn add(self, other: Offset) -> Self::Output {
        Beacon { x: self.x + other.x, y: self.y + other.y, z: self.z + other.z }
    }
}

impl Sub<Beacon> for Beacon {
    type Output = Offset;
    fn sub(self, other: Beacon) -> Self::Output {
        Offset { x: self.x - other.x, y: self.y - other.y, z: self.z - other.z }
    }
}

#[derive(Debug)]
struct Scanner {
    num: i32,
    beacons: Vec<Beacon>,
}

impl Scanner {
    fn from_reader<R: BufRead>(mut reader: R) -> Result<Option<Self>, Error> {
        lazy_static! {
            static ref RE: Regex = Regex::new(r"--- scanner (\d+) ---$").unwrap();
        }

        let mut line = String::new();
        reader.read_line(&mut line)?;

        let line_trim = line.trim_end();
        if line_trim.is_empty() {
            return Ok(None);
        }

        let captures = RE.captures(line_trim).ok_or_else(|| anyhow!("Failed to match Scanner line"))?;

        let num_str = captures.get(1).unwrap().as_str();
        let num = i32::from_str(num_str).unwrap();

        let mut beacons = Vec::new();
        loop {
            let beacon = match Beacon::from_reader(&mut reader)? {
                Some(beacon) => beacon,
                None => break,
            };

            beacons.push(beacon);
        }

        beacons.sort();

        Ok(Some(Scanner { num, beacons }))
    }
}

fn read_scanners<R: BufRead>(mut reader: R) -> Result<Vec<Scanner>, Error> {
    let mut scanners = Vec::new();
    loop {
        let scanner = match Scanner::from_reader(&mut reader)? {
            Some(scanner) => scanner,
            None => break,
        };

        scanners.push(scanner);
    }

    Ok(scanners)
}

#[derive(Debug)]
struct Transform {
    m: [i32; 16], // row-major (first row is at 0, 1, 2, 3)
}

impl Transform {
    fn make_translation(offset: Offset) -> Self {
        Transform { m: [1, 0, 0, offset.x, /**/ 0, 1, 0, offset.y, /**/ 0, 0, 1, offset.z, /**/ 0, 0, 0, 1] }
    }

    // When applied, the resulting Transform will do 'xform' FOLLOWED BY 'self'
    fn combine(&self, xform: &Transform) -> Transform {
        let mut result = Transform { m: [0; 16] };

        for r in 0..4 {
            for c in 0..4 {
                let mut val = 0;
                for i in 0..4 {
                    val += self.m[r * 4 + i] * xform.m[i * 4 + c];
                }

                result.m[r * 4 + c] = val;
            }
        }

        result
    }

    fn apply(&self, beacon: &Beacon) -> Beacon {
        // C = A * B
        // A is m x n (3 x 3) (raws x cols)
        // B is n x p (3 x 1)
        let beacon_w = 1;
        let x = beacon.x * self.m[0] + beacon.y * self.m[1] + beacon.z * self.m[2] + beacon_w * self.m[3];
        let y = beacon.x * self.m[4] + beacon.y * self.m[5] + beacon.z * self.m[6] + beacon_w * self.m[7];
        let z = beacon.x * self.m[8] + beacon.y * self.m[9] + beacon.z * self.m[10] + beacon_w * self.m[11];
        let _w = beacon.x * self.m[12] + beacon.y * self.m[13] + beacon.z * self.m[14] + beacon_w * self.m[15];
        Beacon { x, y, z }
    }

    fn all() -> Vec<Transform> {
        let mut result = Vec::new();

        // This produces 8 * 6 = 48 transforms while the problem says that there are 24.
        // So some of these don't make sense, and hopefully the bad transforms don't actually end up aligning.
        for neg in 0..8 {
            result.push(Transform { m: [1, 0, 0, 0, /**/ 0, 1, 0, 0, /**/ 0, 0, 1, 0, /**/ 0, 0, 0, 1] }); // x->x, y->y, z->z
            result.push(Transform { m: [1, 0, 0, 0, /**/ 0, 0, 1, 0, /**/ 0, 1, 0, 0, /**/ 0, 0, 0, 1] }); // x->x, y->z, z->y

            result.push(Transform { m: [0, 1, 0, 0, /**/ 1, 0, 0, 0, /**/ 0, 0, 1, 0, /**/ 0, 0, 0, 1] }); // x->y, y->x, z->z
            result.push(Transform { m: [0, 1, 0, 0, /**/ 0, 0, 1, 0, /**/ 1, 0, 0, 0, /**/ 0, 0, 0, 1] }); // x->y, y->z, z->x

            result.push(Transform { m: [0, 0, 1, 0, /**/ 1, 0, 0, 0, /**/ 0, 1, 0, 0, /**/ 0, 0, 0, 1] }); // x->z, y->x, z->y
            result.push(Transform { m: [0, 0, 1, 0, /**/ 0, 1, 0, 0, /**/ 1, 0, 0, 0, /**/ 0, 0, 0, 1] }); // x->z, y->y, z->x

            for idx in result.len() - 6..result.len() {
                for axis in 0..3 {
                    if neg & (1 << axis) != 0 {
                        result[idx].m[axis * 4 + 0] = -result[idx].m[axis * 4 + 0];
                        result[idx].m[axis * 4 + 1] = -result[idx].m[axis * 4 + 1];
                        result[idx].m[axis * 4 + 2] = -result[idx].m[axis * 4 + 2];
                    }
                }
            }
        }

        result
    }
}

fn check_alignment(beacons_a: &[Beacon], beacons_b: &[Beacon], off: Offset) -> bool {
    let mut num_aligned = 0;

    for ai in 0..beacons_a.len() {
        for bi in 0..beacons_b.len() {
            if beacons_a[ai] == beacons_b[bi] + off {
                num_aligned += 1;
                break;
            }
        }
    }

    num_aligned >= 12
}

fn align_scanners(scanner_a: &Scanner, scanner_b: &Scanner, xforms: &[Transform], beacons_tmp: &mut Vec<Beacon>) -> Option<Transform> {
    for (xform_i, xform) in xforms.iter().enumerate() {
        beacons_tmp.clear();

        for beacon in scanner_b.beacons.iter() {
            beacons_tmp.push(xform.apply(beacon));
        }

        for ai in 0..scanner_a.beacons.len() {
            for bi in 0..beacons_tmp.len() {
                let off = scanner_a.beacons[ai] - beacons_tmp[bi];
                if check_alignment(&scanner_a.beacons, &beacons_tmp, off) {
                    return Some(Transform::make_translation(off).combine(xform));
                }
            }
        }
    }

    None
}

fn main() -> Result<(), Error> {
    let scanners = read_scanners(stdin().lock())?;
    let xforms = Transform::all();
    let mut beacons_tmp = Vec::new();
    let mut alignments = Vec::new();

    for i in 0..scanners.len() {
        for j in i + 1..scanners.len() {
            if let Some(xform) = align_scanners(&scanners[i], &scanners[j], &xforms, &mut beacons_tmp) {
                println!("aligned {} to {}", scanners[i].num, scanners[j].num);
                alignments.push((i, j, xform));
            }
        }
    }

    println!("{:?}", alignments);

    Ok(())
}
