//Mortal Fibonacci Rabbits
//http://rosalind.info/problems/fibd/


//a bunny takes one month to become mature, and then has a breeding pair of
//children a month later.
struct Bunny {
    id: u32,
    age: u32,
}

//a new bunny will have a new id and will start at 0 months old, of course.
impl Bunny {
    fn new(id: u32) -> Bunny {
        Bunny {
            id: id,
            age: 0,
        }
    }
}


//the scary binary tree stuff. eugghghaaffkjaldfjaskfjasfj
// https://gist.github.com/aidanhs/5ac9088ca0f6bdd4a370
struct Node<'a> {               //ok so this is complicated. /'a/ denotes a
    val: &'a Bunny,             //named lifetime expectancy.
    l: Option<Box<Node<'a>>>,   //Box, allocates memory on the heap. Cool.
    r: Option<Box<Node<'a>>>,   //Option is literally 'optional value.'
}

// and the insertion method
impl<'a> Node<'a> {
    pub fn insert(&mut self, new_val: &'a Bunny) {
        if self.val.id == new_val.id {
            return
        }
        let target_node = if new_val.age < self.val.age { &self.l } else { &self.r };
        match target_node {
            &mut Some(ref mut subnode) => subnode.insert(new_val),
            &mut None => {
                let new_node = Node { val: new_val, l: None, r: None };
                let boxed_node = Some(Box::new(new_node));
                *target_node = boxed_node;
            }
        }
    }
}





fn main() {
    let amount_of_bunnies = 0;

    let bunny_one = Bunny::new(amount_of_bunnies + 1);    

    println!("Bunny {} is {} months old.", bunny_one.id, bunny_one.age);
}
