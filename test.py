from saram import Population, Saram

p = Population(2)
p.people[0].partner = p.people[1]
p.people[1].partner = p.people[0]
p.die()
print(p.people[1].attr)
