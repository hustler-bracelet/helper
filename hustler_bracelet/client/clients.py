import config

from pydantic import BaseModel

from .base import APIHttpClient
from .schemas import (
    ActivityDataResponse, 
    ActivityTaskDataResponse, 
    LeaderBoardItem, 
    NicheDataResponse, 
    ActivityDataCreate,
    ActivitySummaryResponse,
    ActivityUserStatusResponse,
    ProofResponse,
    ProofCreate,
    ActivityTaskStatus,
    ActivityTaskCreateData,
    ProofLoadedReasonse,
)


class BaseAPIClient(APIHttpClient):
    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or config.API_BASE_URL

    async def api_request(
        self, 
        endpoint: str, 
        method: str, 
        schema: BaseModel | None = None, 
        many_result: bool = False,
        nullable_result: bool = False,
        data: dict | None = None
    ) -> dict:
        data = await self.request(method, self.base_url + endpoint, data)
        if schema is None:
            return data

        if data is None and nullable_result:
            return None

        if data is None:
            raise ValueError('Data is None')

        if many_result:
            return [schema(**item) for item in data]

        return schema(**data)


class ActivityAPIClient(BaseAPIClient):
    async def get_activities(self, is_active: bool = True) -> list[ActivityDataResponse]:
        return await self.api_request(
            endpoint=f'/activities?is_active={is_active}',
            method='GET',
            schema=ActivityDataResponse,
            many_result=True,
        )

    async def stop_activity(self, activity_id: int):
        await self.api_request(
            endpoint=f'/activities/{activity_id}/stop',
            method='POST',
            schema=None,
        )

    async def run_activity(self, activity_id: int):
        await self.api_request(
            endpoint=f'/activities/{activity_id}/run',
            method='POST',
            schema=None,
        )

    async def get_activity_user_summary(self, user_id: int, activity_id: int) -> ActivitySummaryResponse:
        return await self.api_request(
            endpoint=f'/users/{user_id}/activities/{activity_id}/summary',
            method='GET',
            schema=ActivitySummaryResponse,
            nullable_result=True,
        )

    async def get_current_activity(self, activity_id: int) -> ActivityDataResponse:
        return await self.api_request(
            endpoint=f'/activities/{activity_id}',
            method='GET',
            schema=ActivityDataResponse,
            nullable_result=True,
        )

    async def get_current_activity(self) -> ActivityDataResponse:
        return await self.api_request(
            endpoint=f'/activities/current',
            method='GET',
            schema=ActivityDataResponse,
            nullable_result=True,
        )

    async def leave_activity(self, user_id: int, activity_id: int):
        await self.api_request(
            endpoint=f'/activities/{activity_id}/leave',
            method='POST',
            schema=None,
            data={'telegram_id': user_id},
            nullable_result=True,
        )

    async def activity_status(self, activity_id: int, user_id: int) -> ActivityUserStatusResponse:
        return await self.api_request(
            endpoint=f'/activities/{activity_id}/status',
            method='GET',
            schema=ActivityUserStatusResponse,
            data={'telegram_id': user_id},
        )


class ActivityTasksAPIClient(BaseAPIClient):
    async def get_current_task(self, niche_id: int) -> ActivityTaskDataResponse:
        return await self.api_request(
            endpoint=f'/niches/{niche_id}/tasks/current',
            method='GET',
            schema=ActivityTaskDataResponse,
        )

    async def get_all_tasks(self, user_id: int, niche_id: int) -> list[ActivityTaskDataResponse]:
        return await self.api_request(
            endpoint=f'/niches/{niche_id}/tasks',
            method='GET',
            schema=ActivityTaskDataResponse,
            many_result=True,
            data={'telegram_id': user_id},
        )

    async def create_new_task(self, niche_id: int, activity_task: ActivityTaskCreateData) -> ActivityTaskDataResponse:
        data = activity_task.model_dump()
        data['deadline'] = data['deadline'].isoformat()

        print(data)

        return await self.api_request(
            endpoint=f'/niches/{niche_id}/tasks',
            method='POST',
            schema=ActivityTaskDataResponse,
            data=data,
        )

    async def get_status_for_user(self, user_id: int, task_id: int) -> ActivityTaskStatus:
        return await self.api_request(
            endpoint=f'/tasks/{task_id}/status',
            method='GET',
            schema=ActivityTaskStatus,
            data={'telegram_id': user_id},
        )

    async def cancel_task(self, user_id: int, task_id: int):
        await self.api_request(
            endpoint=f'/tasks/{task_id}/cancel',
            method='POST',
            schema=None,
            data={'telegram_id': user_id},
        )


class LeaderboardAPIClient(BaseAPIClient):
    async def get_leaderboard(self, activity_id: int) -> list[LeaderBoardItem]:
        return await self.api_request(
            endpoint=f'/activities/{activity_id}/leaderboard',
            method='GET',
            schema=LeaderBoardItem,
            many_result=True,
        )


class NichesAPIClient(BaseAPIClient):
    async def get_niche_by_id(self, niche_id: int) -> NicheDataResponse:
        return await self.api_request(
            endpoint=f'/niches/{niche_id}',
            method='GET',
            schema=NicheDataResponse,
        )

    async def select_niche_by_id(self, user_id: int, niche_id: int) -> NicheDataResponse:
        return await self.api_request(
            endpoint=f'/niches/{niche_id}/select',
            method='POST',
            schema=NicheDataResponse,
            data={'telegram_id': user_id},
        )

    async def get_user_niches(self, user_id: int) -> NicheDataResponse:
        return await self.api_request(
            endpoint=f'/users/{user_id}/niches',
            method='GET',
            schema=NicheDataResponse,
            nullable_result=True,
        )


class ProofsAPIClient(BaseAPIClient):
    async def create_proof(self, proof: ProofCreate) -> ProofResponse:
        return await self.api_request(
            endpoint=f'/proofs',
            method='POST',
            schema=ProofResponse,
            data=proof.model_dump(),
        )

    async def get_proof_by_id(self, proof_id: int) -> ProofResponse:
        return await self.api_request(
            endpoint=f'/proofs/{proof_id}',
            method='GET',
            schema=ProofResponse,
            nullable_result=True,
        )

    async def get_proofs_waitlist(self, activity_id: int) -> list[ProofLoadedReasonse]:
        return await self.api_request(
            endpoint=f'/activities/{activity_id}/proofs/waitlist',
            method='GET',
            schema=ProofLoadedReasonse,
            many_result=True,
        )

    async def accept_proof(self, proof_id: int, extra_points: int = 0):
        await self.api_request(
            endpoint=f'/proofs/{proof_id}/accept?extra_points={extra_points}',
            method='POST',
            schema=None,
        )

    async def decline_proof(self, proof_id: int):
        await self.api_request(
            endpoint=f'/proofs/{proof_id}/reject',
            method='POST',
            schema=None,
        )
