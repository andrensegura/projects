use std::thread::sleep_ms;

const CLEAR: &'static str = "\u{1B}[1;1H\u{1B}[2J";

struct Player {
    icon: char,
    x: u8,
    y: u8,
}

fn main() {
    let mut map = [[' '; 15]; 15];
    let mut player = Player { icon: '@', x: 6, y: 13 };

    for _ in 1..10 {
        set_entity(&mut map, &player);
        draw_map(map);
        sleep_ms(500);
        clear_map(&mut map);
        player.y -= 1;
    }

}

fn clear() {
    println!("{}", CLEAR);
}

fn clear_map(grid: &mut [[char; 15];15]) {
    for i in 0..grid.len() {
        for j in 0..grid[i].len() {
            grid[i][j] = ' ';
        }
    }
}

fn draw_map(grid: [[char; 15];15]) {
    clear();
    for i in 0..grid.len() {
        for j in 0..grid[i].len() {
            print!("{}", grid[i][j]);
        }
        println!("");
    }
}

fn set_entity(grid: &mut [[char; 15];15], entity: &Player) {
    grid[entity.y as usize][entity.x as usize] = entity.icon;

}
