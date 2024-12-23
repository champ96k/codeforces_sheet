import 'dart:convert';

import 'package:codeforces_sheet/model/problem_model.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';

class DataService {
  Future<List<Problem>> loadProblems() async {
   try {
      final String result = await rootBundle.loadString('assets/problems.json');
    final dynamic  data = json.decode(result);
    final problemMap = data as Map<String, dynamic>;

    List<Problem> problemList = [];

    problemMap.forEach((category, problems) {
      final List<Problem> categoryProblems = (problems as List<dynamic>).map<Problem>((e) {
        return Problem.fromJson(e as Map<String, dynamic>);
      }).toList();
      problemList.addAll(categoryProblems);
    });

    return problemList;
   } catch (e) {
    debugPrint('Error: $e');
     throw Exception('Failed to load problems');
   }
  }
}
