use anyhow::{anyhow, Error};
use std::io::{self, BufRead};
use std::str::FromStr;
use std::collections::HashSet;

const PART2: bool = true;

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
struct Node {
    name: String,
}

impl Node {
    fn is_small(&self) -> bool {
        self.name == self.name.to_lowercase()
    }

    fn is_start(&self) -> bool {
        self.name == "start"
    }

    fn is_end(&self) -> bool {
        self.name == "end"
    }
}

impl FromStr for Node {
    type Err = Error;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let name = s.to_string();
        Ok(Node { name })
    }
}

struct Edge {
    node_a: Node,
    node_b: Node,
}

impl Edge {
    fn other_node(&self, node: &Node) -> Option<&Node> {
        if node == &self.node_a {
            return Some(&self.node_b);
        }

        if node == &self.node_b {
            return Some(&self.node_a);
        }

        None
    }

}

impl FromStr for Edge {
    type Err =  Error;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut tokens = s.split('-').map(|t| t.to_string()).collect::<Vec<String>>();
        let mut drain = tokens.drain(..);
        let node_a_str= drain.next().ok_or_else(|| anyhow!("Wrong number of tokens"))?;
        let node_b_str = drain.next().ok_or_else(|| anyhow!("Wrong number of tokens"))?;
        let node_a = Node::from_str(&node_a_str)?;
        let node_b = Node::from_str(&node_b_str)?;
        Ok(Edge { node_a, node_b })
    }
}

fn has_two_small_caves(path: &[Node]) -> bool {
    let mut seen = HashSet::new();

    for node in path {
        if node.is_small() {
            if seen.contains(node) {
                return true;
            }

            seen.insert(node.clone());
        }
    }

    return false;
}

fn walk(edges: &Vec<Edge>, path: &[Node], result: &mut Vec<Vec<Node>>) {
    let last_node = path.last().unwrap();

    if last_node.is_end() {
        result.push(path.to_vec());
        return
    }

    for edge in edges {
        if let Some(other) = edge.other_node(last_node) {
            if other.is_small() {
                if PART2 {
                    let max_visits = if other.is_start() || other.is_end() || has_two_small_caves(path) {
                        1
                    } else {
                        2
                    };

                    if path.iter().filter(|n| &other == n).count() >= max_visits {
                        continue;
                    }
                } else {
                    if path.iter().find(|n| &other == n).is_some() {
                        continue;
                    }
                }
            }

            let mut new_path = path.to_vec();
            new_path.push(other.clone());
            walk(edges, &new_path, result);
        }
    }
}

fn main() -> Result<(), Error> {
    let lines = io::stdin().lock().lines()
        .collect::<Result<Vec<String>, io::Error>>()?;
    let edges = lines.iter().map(|line| Edge::from_str(line))
        .collect::<Result<Vec<Edge>, Error>>()?;
    let path = vec![ Node::from_str("start")? ];
    let mut result = Vec::new();
    walk(&edges, &path, &mut result);

    for path in &result {
        let mut path_str = String::new();
        for node in path {
            if !path_str.is_empty() {
                path_str.push(',');
            }

            path_str.push_str(&node.name);
        }

        println!("{}", path_str);
    }

    Ok(())
}
