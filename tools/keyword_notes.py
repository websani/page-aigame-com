from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    """Represents a structured keyword note with metadata."""
    keyword: str
    description: str
    url: str = ""
    category: str = "general"
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    importance: int = 3  # 1-5 scale

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.importance < 1:
            self.importance = 1
        elif self.importance > 5:
            self.importance = 5

    def formatted_brief(self) -> str:
        """Return a one-line summary of the note."""
        tag_str = ", ".join(self.tags) if self.tags else "none"
        return f"[{self.importance}★] {self.keyword} | {self.category} | tags: {tag_str}"

    def formatted_detailed(self) -> str:
        """Return a multi-line detailed view of the note."""
        lines = [
            f"Keyword:     {self.keyword}",
            f"Description: {self.description}",
            f"URL:         {self.url}",
            f"Category:    {self.category}",
            f"Tags:        {', '.join(self.tags) if self.tags else 'none'}",
            f"Created:     {self.created_at}",
            f"Importance:  {'★' * self.importance}{'☆' * (5 - self.importance)}",
        ]
        return "\n".join(lines)


@dataclass
class NoteCollection:
    """A collection of keyword notes with display and filter utilities."""
    notes: List[KeywordNote] = field(default_factory=list)

    def add(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def filter_by_category(self, category: str) -> List[KeywordNote]:
        return [n for n in self.notes if n.category.lower() == category.lower()]

    def filter_by_importance(self, min_importance: int) -> List[KeywordNote]:
        return [n for n in self.notes if n.importance >= min_importance]

    def export_all_brief(self, separator: str = "\n") -> str:
        return separator.join(n.formatted_brief() for n in self.notes)

    def export_all_detailed(self, separator: str = "\n---\n") -> str:
        return separator.join(n.formatted_detailed() for n in self.notes)


def demo_sample_notes() -> NoteCollection:
    """Create a sample collection with predefined notes for demonstration."""
    collection = NoteCollection()

    collection.add(KeywordNote(
        keyword="爱游戏体育",
        description="A comprehensive platform for sports gaming and interactive experiences.",
        url="https://page-aigame.com",
        category="sports",
        tags=["gaming", "sports", "interactive"],
        importance=5,
    ))

    collection.add(KeywordNote(
        keyword="Python dataclass",
        description="A decorator that generates special methods for classes.",
        url="https://docs.python.org/3/library/dataclasses.html",
        category="programming",
        tags=["python", "dataclass", "struct"],
        importance=4,
    ))

    collection.add(KeywordNote(
        keyword="GitHub repository",
        description="Hosting for version control and collaboration.",
        url="https://github.com",
        category="devops",
        tags=["git", "repository", "collaboration"],
        importance=3,
    ))

    return collection


def format_notes_as_report(notes: List[KeywordNote], title: str = "Keyword Notes Report") -> str:
    """Generate a text report from a list of notes."""
    header = f"=== {title} ===\n"
    body = "\n".join(n.formatted_detailed() for n in notes)
    footer = f"\n=== End of Report ({len(notes)} notes) ==="
    return header + body + footer


if __name__ == "__main__":
    collection = demo_sample_notes()

    print("=== Brief Overview ===")
    print(collection.export_all_brief())

    print("\n\n=== Detailed View of '爱游戏体育' ===")
    for note in collection.filter_by_keyword("爱游戏体育"):
        print(note.formatted_detailed())

    print("\n\n=== Filtered by importance >= 4 ===")
    for note in collection.filter_by_importance(4):
        print(note.formatted_brief())

    print("\n\n=== Full Report ===")
    print(format_notes_as_report(collection.notes, "Demo Notes"))