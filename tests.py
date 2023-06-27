from vectordb.retrieval_qa import regulations_tool
import xmltodict

tests = [
    {
        "input": """
            Silvercrest Petroleum (“Silvercrest”) is an American company that provides services for the oil and gas industry.
            Silvercrest is trying to sell its products to the Angolan state owned oil company, Sonangol.
            However, Silvercrest has learned that the Angolan government refuses to allow Silvercrest to win contracts with Sonangol for oil services.
            Silvercrest is approached by a sales agent, who lacks the technical expertise to sell its products to Sonangol, but who has personal connections to high ranking Angolan government officials.
            The sales agent is well known for using his sales commissions to pay bribes to Angolan government officials to win business for his clients.
            Pay sales commissions to the Angolan sales agent.
            """,
        "status": False,
    },
    {
        "input": """My company operates a number of gaming brands, including the PokerStars online poker website.
            I want to pay $8.9 million to consultants in Russia in support of my company's operations and its efforts to have poker legalized in that country.""",
        "status": False,
    },
    {
        "input": """I would like to buy ice cream for my friend's birthday party.""",
        "status": True,
    },
    {
        "input": """I would like to pay a foreign official for expediting the review of my building permit. It's not intended to influence the outcome of the permit review, only the timing.""",
        "status": True,
    },
]

for test in tests:
    observation = regulations_tool.run(test["input"], verbose=True)
    compliance_response = xmltodict.parse(observation)
    compliance_status = compliance_response.get("response").get("compliance_status")
    print((compliance_status.lower() == "true") == test["status"])
