# Copyright 2022 AntoineMartin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
from typing import List

ADJECTIVES = [
    "baggy",
    "beady",
    "bluesy",
    "blurry",
    "boozy",
    "breezy",
    "bumpy",
    "cheeky",
    "chewy",
    "chummy",
    "clammy",
    "cloudy",
    "cozy",
    "crabby",
    "craggy",
    "cranky",
    "crappy",
    "dorky",
    "droopy",
    "flabby",
    "flaky",
    "flimsy",
    "foggy",
    "freaky",
    "frumpy",
    "fuzzy",
    "gamy",
    "geeky",
    "gimpy",
    "gloppy",
    "goopy",
    "greasy",
    "grumpy",
    "gummy",
    "hasty",
    "hazy",
    "hilly",
    "homely",
    "homey",
    "jumpy",
    "lanky",
    "leaky",
    "lousy",
    "lovely",
    "lumpy",
    "messy",
    "muggy",
    "muzzy",
    "nerdy",
    "nippy",
    "paltry",
    "pasty",
    "pokey",
    "pretty",
    "queasy",
    "randy",
    "ready",
    "scaly",
    "scanty",
    "scummy",
    "seedy",
    "shabby",
    "shaggy",
    "shaky",
    "sickly",
    "silly",
    "skanky",
    "skimpy",
    "skinny",
    "slaphappy",
    "sleazy",
    "sleepy",
    "slimy",
    "sloppy",
    "smelly",
    "snappy",
    "snazzy",
    "snippy",
    "snoopy",
    "squeaky",
    "squirrely",
    "stealthy",
    "stinky",
    "stuffy",
    "sunny",
    "surly",
    "tacky",
    "tasty",
    "thirsty",
    "trippy",
    "ugly",
    "wheezy",
    "whiny",
    "wiggy",
    "wimpy",
    "woolly",
    "woozy",
    "zippy",
]

ANIMALS = [
    "abyssinian",
    "affenpinscher",
    "akbash",
    "akita",
    "albatross",
    "alligator",
    "angelfish",
    "angora",
    "ant",
    "anteater",
    "antelope",
    "argentino",
    "armadillo",
    "audemer",
    "avocet",
    "axolotl",
    "baboon",
    "badger",
    "balinese",
    "bandicoot",
    "barb",
    "barnacle",
    "barracuda",
    "bat",
    "beagle",
    "bear",
    "beaver",
    "bee",
    "beetle",
    "binturong",
    "bird",
    "birman",
    "bison",
    "bloodhound",
    "blue",
    "boar",
    "bobcat",
    "bombay",
    "bongo",
    "bonobo",
    "booby",
    "bordeaux",
    "bracke",
    "budgerigar",
    "buffalo",
    "bulldog",
    "bullfrog",
    "burmese",
    "butterfly",
    "buzzard",
    "caiman",
    "camel",
    "capuchin",
    "capybara",
    "caracal",
    "cassowary",
    "cat",
    "caterpillar",
    "catfish",
    "cattle",
    "centipede",
    "chameleon",
    "chamois",
    "cheetah",
    "chicken",
    "chihuahua",
    "chimpanzee",
    "chin",
    "chinchilla",
    "chinook",
    "chipmunk",
    "chow",
    "cichlid",
    "civet",
    "clam",
    "coati",
    "cockroach",
    "collie",
    "coral",
    "corgi",
    "cougar",
    "cow",
    "coyote",
    "crab",
    "crane",
    "crocodile",
    "cuscus",
    "cuttlefish",
    "dachsbracke",
    "dachshund",
    "dalmatian",
    "dane",
    "deer",
    "devil",
    "dhole",
    "dingo",
    "discus",
    "dodo",
    "dog",
    "dogfish",
    "dollar",
    "dolphin",
    "donkey",
    "dormouse",
    "dragon",
    "dragonfly",
    "drever",
    "duck",
    "dugong",
    "dunker",
    "eagle",
    "earwig",
    "echidna",
    "eel",
    "elephant",
    "eleuth",
    "emu",
    "falcon",
    "ferret",
    "fish",
    "flamingo",
    "flounder",
    "fly",
    "forest",
    "fossa",
    "fousek",
    "fowl",
    "fox",
    "foxhound",
    "frigatebird",
    "frise",
    "frog",
    "gar",
    "gecko",
    "gerbil",
    "gharial",
    "gibbon",
    "giraffe",
    "goat",
    "goose",
    "gopher",
    "gorilla",
    "grasshopper",
    "greyhound",
    "grouse",
    "guppy",
    "hamster",
    "hare",
    "harrier",
    "havanese",
    "hedgehog",
    "heron",
    "hippopotamus",
    "hornet",
    "horse",
    "hound",
    "hummingbird",
    "husky",
    "hyena",
    "hyrax",
    "ibis",
    "iguana",
    "impala",
    "indri",
    "insect",
    "jackal",
    "jaguar",
    "javanese",
    "jellyfish",
    "kakapo",
    "kangaroo",
    "kingfisher",
    "kiwi",
    "koala",
    "kudu",
    "labradoodle",
    "ladybird",
    "lemming",
    "lemur",
    "leopard",
    "liger",
    "lion",
    "lionfish",
    "lizard",
    "llama",
    "lobster",
    "loon",
    "lynx",
    "macaque",
    "macaw",
    "magpie",
    "malamute",
    "maltese",
    "mammoth",
    "manatee",
    "mandrill",
    "markhor",
    "mastiff",
    "mau",
    "mayfly",
    "meerkat",
    "millipede",
    "mist",
    "mole",
    "molly",
    "mongoose",
    "mongrel",
    "monkey",
    "monster",
    "moorhen",
    "moose",
    "moth",
    "mouse",
    "mule",
    "neanderthal",
    "newfoundland",
    "newt",
    "nightingale",
    "numbat",
    "ocelot",
    "octopus",
    "okapi",
    "olm",
    "opossum",
    "orangutan",
    "oriole",
    "ostrich",
    "otter",
    "owl",
    "oyster",
    "panda",
    "paradise",
    "peccary",
    "penguin",
    "pig",
    "pinscher",
    "quail",
    "quetzal",
    "quokka",
    "quoll",
    "rabbit",
    "raccoon",
    "ragdoll",
    "rat",
    "rattlesnake",
    "ray",
    "reindeer",
    "retriever",
    "rhinoceros",
    "robin",
    "rottweiler",
    "russel",
    "salamander",
    "saola",
    "schnauzer",
    "scorpion",
    "seahorse",
    "seal",
    "serval",
    "setter",
    "shark",
    "sheep",
    "sheepdog",
    "shrew",
    "shrimp",
    "skunk",
    "sloth",
    "slug",
    "snail",
    "snake",
    "spaniel",
    "sparrow",
    "spider",
    "spitz",
    "sponge",
    "spoonbill",
    "squid",
    "squirrel",
    "squirt",
    "starfish",
    "stingray",
    "stoat",
    "swan",
    "tamarin",
    "tang",
    "tapir",
    "tarantula",
    "tarsier",
    "termite",
    "terrier",
    "tetra",
    "tiger",
    "toad",
    "tortoise",
    "toucan",
    "tuatara",
    "turkey",
    "turtle",
    "tzu",
    "uakari",
    "uguisu",
    "urchin",
    "vole",
    "vulture",
    "wallaby",
    "walrus",
    "warthog",
    "wasp",
    "weasel",
    "whale",
    "whippet",
    "wildebeest",
    "wolf",
    "wolfhound",
    "wolverine",
    "wombat",
    "woodlouse",
    "woodpecker",
    "worm",
    "wrasse",
    "yak",
    "zebra",
    "zebu",
    "zonkey",
    "zorse",
]


def generate_name(repeat_parts=False, separator="-", lists=(ADJECTIVES, ANIMALS)):
    """Generate a single random name.

    :type repeat_parts: bool
    :param repeat_parts: If set, do not ensure that each part of the name
                         is unique to the name itself.
    :type separator: str
    :param separator: The string that is used to join each part of the name.
    :type lists: list of lists
    :param lists: A list of dictionary lists that will be used for each
                  part of the name. One word is chosen from each list in
                  order.
    """
    name: List[str] = []
    for lyst in lists:
        part = None
        while not part or (part in name and not repeat_parts):
            part = random.choice(lyst)
        name.append(part)
    return separator.join(name)
