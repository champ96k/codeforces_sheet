class Problem {
  final String title;
  final String link;
  final List<String> tags;
  final String difficulty;

  Problem({
    required this.title,
    required this.link,
    required this.tags,
    required this.difficulty,
  });

  factory Problem.fromJson(Map<String, dynamic> json) {
    return Problem(
      title: json['title'],
      link: json['link'],
      tags: List<String>.from(json['tags']),
      difficulty: json['difficulty'],
    );
  }
}
