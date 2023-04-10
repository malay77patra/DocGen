import openai


def explain_code(API_KEY, typo, snifft):
  openai.api_key = API_KEY
  output = ""
  api_settings = {
    "engine": "text-davinci-003",
    "max_tokens": 2048,
    "n": 1,
    "stop": None,
    "temperature": 0.3,
  }
  if typo == "imports":
    prompt = (
      f"Explain each modules of given list of import statements from a big script file in markdown format, use different symbols to make look nice, must include small headins #\ngiven:\n{snifft}"
    )
    response = openai.Completion.create(
      prompt=prompt,
      **api_settings,
    )
    output += response.choices[0].text.strip()

  elif typo == "variables":
    prompt = (
      f"Explain each variables of given list of declearations from a big script file in markdown format, use different symbols to make look nice, must include small headins #, explain the use of operators used, and data type of variable \ngiven:\n{snifft}"
    )
    response = openai.Completion.create(
      prompt=prompt,
      **api_settings,
    )
    output += response.choices[0].text.strip()
  elif typo == "functions":
    for func in snifft:
      prompt = (
        f"Please explain in detailsthe following function in Markdown format which is a part of a big script file. You should include # headings, introduction, all the parameters, working, all input and outpu, examples, use different type of symbols and indent to respresent it nicely, any extra data if needed \nGiven class:\n{snifft}"
      )
      response = openai.Completion.create(
        prompt=prompt,
        **api_settings,
      )
      output += "\n***\n" + response.choices[0].text.strip()

  elif typo == "classes":
    for cls in snifft:
      prompt = (
        f"Please explain in detailsthe following class in Markdown format which is a part of a big script file. You should include # headings, introduction, all the parameters, all functions, examples, all input and outpu,uae different type of symbols and indent to respresent it nicely, any extra data if needed \nGiven class:\n{snifft}"
      )
      response = openai.Completion.create(
        prompt=prompt,
        **api_settings,
      )
      output += "\n***\n" + response.choices[0].text.strip()

  return output


#outdata = explain_code(API_KEY, "classes", snifft)
