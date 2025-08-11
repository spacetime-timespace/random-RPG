console.log('Hello World')

for(let i = 0; i < 3; i++){
  console.log(i)
}

i = {name: "Bob", age: "42"}
console.log(i.name,i.age)

class Skibidis{
  constructor(level,rizz){
    this.level = level
    this.rizz = rizz
  }
  toString(){
    return   `Skibidi Level ${this.level} with aura level ${this.rizz}`
  }
}

alex = new Skibidi(1000,999)
console.log(alex.toString())
