Class Category(BaseModel):
    id: int
    name: str
    level: Literal['primary', 'secondary', 'tertiary']
    parent_id: Optional[int] = None