
// ignore_for_file: deprecated_member_use

import 'package:flutter/material.dart';
import 'package:codeforces_sheet/model/problem_model.dart';
import 'package:codeforces_sheet/services/data_services.dart';

class ProblemList extends StatefulWidget {
  const ProblemList({super.key});

  @override
  State<ProblemList> createState() => _ProblemListState();
}

class _ProblemListState extends State<ProblemList> {
  late Future<List<Problem>> _problems;

  @override
  void initState() {
    super.initState();
    _problems = DataService().loadProblems();
  }

  String getDifficultyText(int? difficulty) {
    if (difficulty == null) {
      return 'Unknown';
    }

    if (difficulty < 800) return 'School';
    if (difficulty < 1000) return 'Basic';
    if (difficulty < 1200) return 'Easy';
    if (difficulty < 1500) return 'Medium';
    if (difficulty < 2000) return 'Hard';
    if (difficulty < 2500) return 'Hard - ||';
    if (difficulty < 3000) return 'Hard - |||';
    if (difficulty < 3500) return 'Hard - ||||';
    if (difficulty < 4000) return 'Hard - V|';
    return 'Unknown';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Problems'),
        backgroundColor: Colors.blueAccent,
      ),
      body: FutureBuilder<List<Problem>>(
        future: _problems,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }

          if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('No problems available.'));
          }

          final problems = snapshot.data!;

          return ListView.builder(
            padding: const EdgeInsets.all(0.0),
            shrinkWrap: true,
            itemCount: problems.length,
            itemBuilder: (context, index) {
              final problem = problems[index];
              return Container(
            decoration: BoxDecoration(
              color: index % 2 == 0 ? Colors.black.withOpacity(0.7) : Colors.black87,
            ),
            child: ListTile(
              contentPadding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
              leading: Text(
                '${index + 1} - ${problem.title}',
                style: const TextStyle(color: Colors.white),
              ),
              trailing: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  ...problem.tags.map((tag) => Padding(
                    padding: const EdgeInsets.only(right: 8),
                    child: Text(tag,
                    style:  TextStyle(
                      color: Colors.yellow
                    ),
                    ),
                  ),),
                  const SizedBox(width: 16),
                  _buildDifficultyChip(index),
                ],
              ),
            ),
          );
            },
          );
        },
      ),
    );
  }


  
  Widget _buildDifficultyChip(int i) {
    final index = i % 13;
    final difficulties = [
      'Medium',
      'Easy',
      'Medium',
      'Medium',
      'Hard',
      'Medium',
      'Medium',
      'Medium',
      'Easy',
      'Hard',
      'Medium',
      'Medium',
      'Easy',
    ];

    final color = {
      'Easy': Colors.green,
      'Medium': Colors.orange,
      'Hard': Colors.red,
    };

    return Chip(
      label: Text(
        difficulties[index],
        style: const TextStyle(color: Colors.white),
      ),
      backgroundColor: color[difficulties[index]],
    );
  }

}

class ProblemWebView extends StatelessWidget {
  final String url;

  const ProblemWebView({super.key, required this.url});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Problem'),
      ),
      // body: WebView(
      //   initialUrl: url,
      // ),
    );
  }
}