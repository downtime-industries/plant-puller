from haystack.nodes import PromptNode

def answer_question(question):
  # Initalize the node passing the model:
  prompt_node = PromptNode(model_name_or_path="google/flan-t5-large", model_kwargs={"model_max_length" : 2048})

  # Go ahead and ask a question:
  output = prompt_node(question)

  return output[0]

if __name__=="__main__":
  cleaner_prompt = """
  Question: Read the following context and remove any text that seems to be related 
            to the formatting of the document. Keep all the data needed to answer 
            the question "plant names that are identified as being good houseplants". 
  Context: ng/g40742429/best-indoor-plants-for-health/?slide=3","description":"Rubber plants — also known as rubber trees or Ficus elastica — make for great indoor houseplants. They’re generally easy to take care of and only need to be watered every week or so, according to materials shared by The Sill. Research shows that rubber plants feature air-purifying properties. Just be sure to keep them firmly away from any pets and from young children, as they're known to be highly toxic when ingested.SHOP RUBBER PLANT","image":"https://hips.hearstapps.com/hmg-prod/images/ficus-elastic-plant-rubber-tree-in-white-ceramic-royalty-free-image-1659025626.jpg"}},{"@type":"ListItem","position":4,"item":{"@type":"Thing","name":"Elephant Ear Plants","url":"https://www.goodhousekeeping.com/home/gardening/g40742429/best-indoor-plants-for-health/?slide=4","description":"If you want to spend a little more time with your houseplants, Cromer recommends elephant ear plants. These are organized into a group of tropical, perennial plants instantly recognizable by their big, heart-shaped leaves. They need bright light and regular watering to keep the soil moist, and they can get big and may need extra space. Some species have been grown for their edible starchy tubers, which are a food staple in certain tropical regions. Medicinally, the leaves have been noted for their use in treating insect stings.SHOP ELEPHANT EAR PLANT","image":"https://hips.hearstapps.com/hmg-prod/images/alocasia-sanderiana-bull-or-alocasia-bambino-in-a-royalty-free-image-1659026074.jpg"}},{"@type":"ListItem","position":5,"item":{"@type":"Thing","name":"Snake Plants","url":"https://www.goodhousekeeping.com/home/gardening/g40742429/best-indoor-plants-for-health/?slide=5","description":"Long known as “mother-in-law’s tongues,” the snake plant, or Sansevieria trifasciata, features tall leaves that grow vertically. They’re decorative and extremely low-maintenance. The plants only need to be watered when the soil is dry, grow in any kind of light, and generally “thrive on neglect,” according to experts at HGTV. The snake plant was included in the same sweeping NASA study of indoor plants, and has been shown to remove toxins from the air over time.SHOP SNAKE PLANT","image":"https://hips.hearstapps.com/hmg-prod/images/potted-snake-plants-inside-a-beautiful-new-flat-or-royalty-free-image-1659026388.jpg"}},{"@type":"ListItem","position":6,"item":{"@type":"Thing","name":"Ferns","url":"https://www.goodhousekeeping.com/home/gardening/g40742429/best-indoor-plants-for-health/?slide=6","description":"A 2022 study published in Applied Sciences showed that Boston ferns performed best when it comes to air cleaning by naturally VOCs from the air. The plants grow easily and look the best indoors in hanging baskets or on pl
  """

  response = answer_question(cleaner_prompt)

  prompt = f"""
  Question: Read the following text in the context section and pull out any plant names 
            that are identified as being good houseplants. The output should be formatted 
            as a newline delimited list. If there are no plants then do not output anything. 
  Context: {response}
  """
  actual = answer_question(prompt)

  print(actual)