from fastapi import APIRouter, HTTPException
from typing import List

from app.notes.service import get_all_notes, get_note_by_id
from app.notes.schemas import NoteRead

router = APIRouter(prefix="/notes", tags=["Нотатки 📝"])


@router.get("/", response_model=List[NoteRead], summary="Отримати список всіх нотаток")
async def list_notes():
    notes = await get_all_notes()
    return notes


@router.get("/{note_id}", response_model=NoteRead, summary="Отримати нотатку за id")
async def retrieve_note(note_id: int):
    note = await get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Нотатку не знайдено.")
    return note
