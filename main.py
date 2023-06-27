from agents.demo_chat_agent import agent_executor
from agents.handler import AgentExecutorHandler

## if main:
if __name__ == "__main__":
    agent_executor_handler = AgentExecutorHandler("chat_session_id", "message_id")

    agent_executor.run(
        **{
            "input": """
            Silvercrest Petroleum (“Silvercrest”) is an American company that provides services for the oil and gas industry. 
            Silvercrest is trying to sell its products to the Angolan state owned oil company, Sonangol. 
            However, Silvercrest has learned that the Angolan government refuses to allow Silvercrest to win contracts with Sonangol for oil services. 
            Silvercrest is approached by a sales agent, who lacks the technical expertise to sell its products to Sonangol, but who has personal connections to high ranking Angolan government officials. 
            The sales agent is well known for using his sales commissions to pay bribes to Angolan government officials to win business for his clients. 
            
            Pay sales commissions to the Angolan sales agent.
            """,
            "callbacks": [
                # agent_executor_handler
            ],
        }
    )
    # working
    agent_executor.run(
        **{
            "input": """My company operates a number of gaming brands, including the PokerStars online poker website. 
            I want to pay $8.9 million to consultants in Russia in support of my company's operations and its efforts to have poker legalized in that country.""",
            "callbacks": [
                # agent_executor_handler
            ],
        }
    )
    # working
    agent_executor.run(
        **{
            "input": """I would like to buy ice cream for my friend's birthday party.""",
            "callbacks": [
                # agent_executor_handler
            ],
        }
    )
    # hard edge case, not working
    agent_executor.run(
        **{
            "input": """I would like to pay a foreign official for expediting the review of my building permit. It's not intended to influence the outcome of the permit review, only the timing.""",
            "callbacks": [
                # agent_executor_handler
            ],
        }
    )
