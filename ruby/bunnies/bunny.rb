$names = IO.readlines "./names.txt"

class Bunny
    @@amount_of_bunnies = 0
    @@amount_of_males = 0
    @@amount_of_females = 0
    @@amount_of_rmv = 0
    def initialize(s, c, n, r)
        @sex = s.to_s
        @age = 0
        @color = c.to_s
        @name = n
        @rmv = r
        @@amount_of_bunnies += 1
        @sex == "male" ? @@amount_of_males += 1 : @@amount_of_females += 1
        @@amount_of_rmv +=1 if @rmv
    end
    def self.amount_of_bunnies; @@amount_of_bunnies; end
    def self.amount_of_males; @@amount_of_males; end
    def self.amount_of_females; @@amount_of_females; end
    def self.amount_of_rmv; @@amount_of_rmv; end
    def sex; @sex; end
    def age; @age; end
    def color; @color; end
    def name; @name; end
    def rmv; @rmv; end
    def older; @age += 1; end
    def turn; @rmv = true ; @@amount_of_rmv += 1 ; end
    def one_less_bunny
        @@amount_of_bunnies -= 1
        @sex == "male" ? @@amount_of_males-=1 : @@amount_of_females-=1
    end
end

def initBunniesArray
    arr = Array.new
    while arr.length != 5 do
        arr << Bunny.new([:"male", :"female"].choice,
                             [:"white", :"black", :"brown", :"spotted"].choice,
                             $names.choice,
                             rand(100) > 2 ? false : true)
    end
    arr
end

def printBunny(bunny)
    puts bunny.name.chomp + ":"
    puts "\tAge: " + bunny.age.to_s
    puts "\tSex: " + bunny.sex
    puts "\tColor: " + bunny.color
    puts "\tRMV: " + bunny.rmv.to_s
end

def killElders
    #need to call bunny.one_less_bunny somehow
    $bunnies.delete_if do |bunny|
        if (bunny.rmv && bunny.age > 50)||(!bunny.rmv && bunny.age > 10)
            bunny.one_less_bunny
        end
    end
end

def infect
    Bunny.amount_of_rmv.times do
        unturned = $bunnies.select { |bunny| bunny.rmv == false }
        unturned.choice.turn if unturned.any?
    end
end

def checkOverpopulation
    if Bunny.amount_of_bunnies >= 1000
        howManyToDie = Bunny.amount_of_bunnies/2
        puts "\nOverpopulation!"
        howManyToDie.times do
            bunny = $bunnies.choice
            bunny.one_less_bunny
            $bunnies.delete(bunny)
        end
        puts howManyToDie.to_s + " died!"
    end
end

def makeBabyBunnies
    females = $bunnies.select {|bunny| bunny.sex == "female" \
                               && !bunny.rmv \
                               && bunny.age >= 2}
    males = $bunnies.select {|bunny| bunny.sex == "male" \
                             && !bunny.rmv \
                             && bunny.age >= 2}

    males.length.times do
        females.each { |bunny|
            $bunnies << Bunny.new([:"male", :"female"].choice,
                                  bunny.color,
                                  $names.choice,
                                  rand(100) > 2 ? false : true) }
    end
end

def step
    #age the bunny!
    $bunnies.each { |bunny| bunny.older }
    killElders
    makeBabyBunnies
    infect
    checkOverpopulation
end


#####################
#   MAIN CODE
#####################

$bunnies = initBunniesArray()

input = 'a'
while input != 'q' do
    if input == 's'
        $bunnies.each { |bunny| printBunny(bunny) }
    elsif input == 'a'
        puts "Amount of Bunnies: " + Bunny.amount_of_bunnies.to_s
        puts "Amount of Males: " + Bunny.amount_of_males.to_s
        puts "Amount of Females: " + Bunny.amount_of_females.to_s
        puts "Amount of RMV: " + Bunny.amount_of_rmv.to_s
    elsif input == 'n'
        step
    elsif input == 'k'
        checkOverpopulation
    elsif input == '?'
        puts "(s)how bunnies, (a)mounts, (n)ext step"
    end
    input = gets.chars.first
end
