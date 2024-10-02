from typing import Dict, List, Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.concurrency import run_in_threadpool
from proofofWork import get_answer_token, get_config
import random
from loguru import logger
app = FastAPI()

class ProofOfWorkRequest(BaseModel):
    proofofwork_seed: str
    proofofwork_diff: str
    config: List[Union[int, str, float, None]]

class ProofOfWorkResponse(BaseModel):
    token: str
    solved: bool

@app.post("/get_proof_of_work", response_model=ProofOfWorkResponse)
async def get_proof_of_work(request: ProofOfWorkRequest):
    
    try:
        token, solved = await run_in_threadpool(
            get_answer_token,
            request.proofofwork_seed,
            request.proofofwork_diff,
            request.config,
        )
        # logger.info(f"Proof of work generated: token={token[:10]}, solved={solved}")  # 添加日志
        return ProofOfWorkResponse(token=token, solved=solved)
    except Exception as e:
        logger.error(f"Error generating proof of work: {str(e)}")  # 添加错误日志
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)