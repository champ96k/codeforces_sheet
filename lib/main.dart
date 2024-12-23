import 'package:codeforces_sheet/view/problem_list.dart';
import 'package:flutter/material.dart';


void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Problem Viewer',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const ProblemList(),
    );
  }
}

