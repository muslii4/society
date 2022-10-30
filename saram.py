import random


class Population:
    EXPECTANCY = 100*365

    HEALTH_ALPHA = 5
    HEALTH_BETA = 1
    ATTR_ALPHA = 2
    ATTR_BETA = 3
    HAPPINESS_ALPHA = 1.4
    HAPPINESS_BETA = 1
    EXPECTANCY_ALPHA = 12
    EXPECTANCY_BETA = 2.5

    def __init__(self, n):
        self.people = []
        self.n = n
        self.peopleEver = n
        self.partnerAges = []
        self.partnerAgeDiff = []
        self.partnerAttr = []
        self.breakupLengths = []
        self.breakups = []
        self.children = []
        self.virgins = 0
        self.generations = []
        self.pregnancyAges = []
        self.suicides = 0
        self.lifeLengths = []
        for i in range(n):
            self.people.append(Saram(maxHealth=random.betavariate(self.HEALTH_ALPHA, self.HEALTH_BETA),
                                     intell=random.uniform(0, 1),
                                     rel=(4 * (random.uniform(0, 1) - 0.5)) ** 2,
                                     expectancy=self.EXPECTANCY * random.betavariate(self.EXPECTANCY_ALPHA, self.EXPECTANCY_BETA),
                                     population=self,
                                     sex=random.randint(0, 1),
                                     attr=random.betavariate(self.ATTR_ALPHA, self.ATTR_BETA),
                                     happiness=random.betavariate(self.HAPPINESS_ALPHA, self.HAPPINESS_BETA)))

    def die(self, person):
        self.breakups.append(person.breakups)
        if person.sex == 0:
            self.children.append(person.children)
        if person.breakups == 0 and person.partner is None:
            self.virgins += 1
        self.generations.append(person.generation)
        self.lifeLengths.append(person.age/365)

        if person.partner is not None:
            person.partner.partner = None
            person.partner.married = False
        self.people.remove(person)
        self.n -= 1

    def add(self, person):
        self.people.append(person)
        self.n += 1
        self.peopleEver += 1

    def day(self):
        for person in self.people:
            person.day()


class Saram:
    def __init__(self, maxHealth, intell, rel, expectancy, population, sex, attr, happiness, gen=1):
        self.maxHealth = maxHealth
        self.health = 1
        self.intell = intell
        self.rel = rel
        self.age = 0
        self.baseHappiness = happiness
        self.happiness = self.baseHappiness
        self.expectancy = expectancy
        self.population = population
        self.partner = None
        self.partnerLength = 0
        self.married = False
        self.sex = sex
        self.attr = attr
        self.breakups = 0
        self.children = 0
        self.pregnancy = 0
        self.generation = gen

    def day(self):
        self.age += 1
        self.maxHealth = ((self.expectancy-self.age)/(self.expectancy-self.age+1)) * self.maxHealth
        if self.age > self.expectancy or self.health <= 0:  # death
            self.population.die(self)

        if self.age > 16 * 365 and self.partner is None:  # finding a partner
            if random.uniform(0, 1) < 0.0075:
                if self.age < (random.betavariate(1, 2) * self.population.EXPECTANCY)*375 and self.attr > random.betavariate(2.2, 1):
                    attr_diff = random.betavariate(1, 5)
                    age_diff = random.betavariate(1, 20) * self.population.EXPECTANCY
                    for i in range(self.population.n - 1):
                        candidate = random.choice(self.population.people)
                        if candidate.partner is None and candidate.sex != self.sex and abs(
                                candidate.age - self.age) < age_diff and abs(
                                candidate.attr - self.attr) < attr_diff and candidate.age > 16*365:
                            self.partner = candidate
                            candidate.partner = self
                            self.population.partnerAges.append(self.age / 365)
                            self.population.partnerAttr.append(self.attr)
                            self.population.partnerAgeDiff.append((self.age - self.partner.age)/365)
                            break

        if self.partner is not None:
            self.partnerLength += 1
            if random.uniform(0, 1) < 0.001:  # breaking up
                if random.betavariate(1, 1.05) * 73*365 * 1/(self.children+1) > self.age:
                    if not self.married or random.uniform(0, 1) < 0.1:
                        self.population.breakupLengths.append(self.partnerLength / 365)
                        self.breakups += 1
                        self.partner.breakups += 1
                        self.partner.partner = None
                        self.partner.partnerLength = 0
                        self.partner = None
                        self.partnerLength = 0
            if random.uniform(0, 1) < 0.001:  # marriage
                if self.partnerLength > random.betavariate(1.5, 1):
                    self.married = True
                    self.partner.married = True

        if self.sex == 0 and self.pregnancy == 0:  # pregnancy
            if self.partner is not None and self.age < 45*365:
                if random.uniform(0, 1) < 0.0015:
                    if 1/((self.children + 1) * 2.3) > random.uniform(0, 1) and self.age < random.betavariate(2, 3) * self.population.EXPECTANCY:
                        self.pregnancy = 1
                        self.population.pregnancyAges.append(self.age/365)
                        self.children += 1
                        self.partner.children += 1
        if 0 < self.pregnancy < 9*30:
            self.pregnancy += 1
        if self.pregnancy == 9*30:
            self.pregnancy = 0
            self.population.add(Saram(maxHealth=(self.health*3 + random.betavariate(self.population.HEALTH_ALPHA, self.population.HEALTH_BETA))/4,
                                      intell=(self.intell*3 + random.uniform(0, 1))/4,
                                      rel=(self.rel*9 + (4 * (random.uniform(0, 1) - 0.5)) ** 2)/10,
                                      expectancy=(self.expectancy + self.population.EXPECTANCY * random.betavariate(
                                          self.population.EXPECTANCY_ALPHA, self.population.EXPECTANCY_BETA))/2,
                                      population=self.population,
                                      sex=random.randint(0, 1),
                                      attr=(self.attr*2 + random.betavariate(self.population.ATTR_ALPHA, self.population.ATTR_BETA))/3,
                                      gen=self.generation + 1,
                                      happiness=random.betavariate(self.population.HAPPINESS_ALPHA, self.population.HAPPINESS_BETA)))

        if random.uniform(0, 1) < 0.000001:  # suicide
            if self.happiness < random.betavariate(1, 20):
                self.population.die(self)
                self.population.suicides += 1
