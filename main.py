from vector_db_operations import settings, get_vector_store
from langchain_core.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain_groq import ChatGroq
import cachetools
from sentence_transformers import CrossEncoder
from langchain.memory import ConversationBufferMemory
import timer


memory = ConversationBufferMemory(memory_key="chat_history", input_key="question")
cross_encoder_model = CrossEncoder(settings.CROSS_ENCDER_MODEL)

cache = cachetools.LRUCache(maxsize=20)

def get_retriever():
    qdrant = get_vector_store()
    return qdrant

def do_similarity_search(query):
    retriver = get_retriever()
    docs = retriver.similarity_search_with_relevance_scores(query, k=settings.RETRIVAL_CHUNKS)
    return docs

def re_rank_results(query, documents):
    pairs = [(query, doc[0].page_content) for doc in documents]
    scores = cross_encoder_model.predict(pairs)
    ranked_results = sorted(zip(scores, documents), key=lambda x: x[0], reverse=True)
    return [doc[0] for _, doc in ranked_results]

def get_chain():
    templet = '''You are an ESG expert chatbot with a comprehensive understanding of Environmental, Social, and Governance principles, frameworks (e.g., GRI, SASB, TCFD), and related concepts. You provide accurate, professional, and concise answers based strictly on the provided context Without making any extra response other than the response that needed. Handle multi-document references seamlessly by without showing any mention of references or citations. If the required information is not in the context, state: "The information is not currently available in the provided documents." Do not fabricate or infer details beyond the context.

    ### Example 1:
    ### Context:
    From ESG Report 2023: "Company Z's total energy consumption in 2023 was 1.2 million kWh, with 40"%" sourced from renewable energy."
    From Sustainability Policy Document: "Company Z aims to increase renewable energy usage to 70"%" by 2025."

    ### User Query:
    What is the current energy consumption of Company Z, and what are its renewable energy targets?

    ### Professional Answer:
    Company Z's total energy consumption in 2023 was 1.2 million kWh, with 40"%" sourced from renewable energy. The company aims to increase renewable energy usage to 70"%" by 2025.

    ---

    ### Example 2:
    ### Context:
    From Annual Sustainability Report: "Company Y has reduced water usage by 15'%' over the last three years."
    From Environmental Goals Document: "Company Y's target is to achieve a 25"%" reduction in water usage by 2025."

    ### User Query:
    How much has Company Y reduced its water usage, and what is its future target?

    ### Professional Answer:
    Company Y has reduced water usage by 15"%" over the last three years. The company aims to achieve a 25"%" reduction in water usage by 2025.

    ---

    ### Example 3:
    ### Context:
    From Social Impact Report: "Company X has a workforce gender diversity ratio of 60:40 (male to female)."
    From Inclusion Strategy Document: "Company X plans to improve female representation to 45"%" by 2026."

    ### User Query:
    What is the current gender diversity ratio at Company X, and what is its goal for the future?

    ### Professional Answer:
    Company X's current workforce gender diversity ratio is 60:40 (male to female). The company plans to improve female representation to 45"%" by 2026.

    ---

    ### Example 4:
    #### Context:
    From ESG Basics Document: "Environmental factors include energy consumption, waste management, and carbon emissions. Social factors involve labor practices, diversity, and community impact. Governance focuses on transparency, board structure, and ethics."

    #### User Query:
    What are the main components of ESG?

    #### Professional Answer:
    The main components of ESG are:  
    - **Environmental**: Energy consumption, waste management, and carbon emissions.  
    - **Social**: Labor practices, diversity, and community impact.  
    - **Governance**: Transparency, board structure, and ethics.

    ---
    
    ### Example 5:
    #### Context:
    From Company Overview Document: "Company A's carbon footprint was 10,000 metric tons of CO2 in 2022. The company has committed to reducing its carbon footprint by 30% by 2030."

    #### User Query:
    What is Company A's current carbon footprint, and what is its reduction goal?

    #### Professional Answer:
    Company A's current carbon footprint is 10,000 metric tons of CO2 (as of 2022). The company has committed to reducing its carbon footprint by 30% by 2030.

    ---

    ### Example 6:
    #### Context:
    From ESG Basics Guide: "Sustainability reporting helps organizations track and communicate their impact on environmental, social, and governance issues. Frameworks like GRI and SASB provide guidelines for such reports."

    #### User Query:
    Why is sustainability reporting important?

    #### Professional Answer:
    Sustainability reporting is important because it helps organizations track and communicate their impact on environmental, social, and governance issues. Frameworks like GRI and SASB provide guidelines to ensure consistency and transparency in these reports.

    ---

    ### Example 7:
    #### Context:
    From Governance Practices Document: "Company B has a 12-member board with 50% independent directors. The company adheres to the highest standards of transparency in its financial disclosures."

    #### User Query:
    What governance practices does Company B follow?

    #### Professional Answer:
    Company B's governance practices include maintaining a 12-member board with 50% independent directors and adhering to the highest standards of transparency in financial disclosures.

    ---


    ### Context:
    {context}

    ### Chat History: 
    {chat_history}
    
    ### User Query:
    {question}

    ### Professional Answer: 
    '''
    prompt = PromptTemplate(template=templet, input_variables=["context", "chat_history","question"])
    llm = ChatGroq(api_key=settings.GROQ_API_KEY)
    return load_qa_chain(llm=llm, chain_type="stuff", prompt=prompt, memory=memory)

def generate_response(query):
    
    if query in cache:
        return(cache[query])

    docs = do_similarity_search(query)
    re_arranged_documents = re_rank_results(query, docs)
    chain = get_chain()
    response = chain.invoke({
        "input_documents": re_arranged_documents,
        "question": query,
        "chat_history": memory.load_memory_variables({})
    })
    result = response.get('output_text')
    cache[query] = result
    return result

while 1:
    question = input("")
    result = generate_response(question)
    print(result)
