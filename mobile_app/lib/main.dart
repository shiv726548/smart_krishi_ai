import 'package:flutter/material.dart';
import 'screens/auth_screen.dart';
import 'screens/dashboard_screen.dart';
import 'screens/plant_scanner_screen.dart';
import 'screens/ai_assistant_screen.dart';
import 'screens/crop_management_screen.dart';
import 'screens/weather_screen.dart';

void main() {
  runApp(const SmartKrishiApp());
}

class SmartKrishiApp extends StatelessWidget {
  const SmartKrishiApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Smart Krishi AI',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        primarySwatch: Colors.green,
        scaffoldBackgroundColor: const Color(0xFF0F172A),
        fontFamily: 'Roboto',
      ),
      home: const MainNavigationWrapper(),
    );
  }
}

class MainNavigationWrapper extends StatefulWidget {
  const MainNavigationWrapper({Key? key}) : super(key: key);

  @override
  _MainNavigationWrapperState createState() => _MainNavigationWrapperState();
}

class _MainNavigationWrapperState extends State<MainNavigationWrapper> {
  bool isLoggedIn = false;
  int _currentIndex = 0;

  final List<Widget> _screens = const [
    DashboardScreen(),
    PlantScannerScreen(),
    AIAssistantScreen(),
    CropManagementScreen(),
    WeatherScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    if (!isLoggedIn) {
      return AuthScreen(
        onLoginSuccess: () => setState(() => isLoggedIn = true),
      );
    }

    return Scaffold(
      body: IndexedStack(
        index: _currentIndex,
        children: _screens,
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) => setState(() => _currentIndex = index),
        type: BottomNavigationBarType.fixed,
        backgroundColor: const Color(0xFF1E293B),
        selectedItemColor: Colors.greenAccent,
        unselectedItemColor: Colors.white54,
        items: const [
          BottomNavigationBarStyle(icon: Icon(Icons.dashboard), label: "Home"),
          BottomNavigationBarStyle(icon: Icon(Icons.center_focus_strong), label: "Scan AI"),
          BottomNavigationBarStyle(icon: Icon(Icons.chat_bubble), label: "Assistant"),
          BottomNavigationBarStyle(icon: Icon(Icons.agriculture), label: "Crops"),
          BottomNavigationBarStyle(icon: Icon(Icons.wb_sunny), label: "Weather"),
        ],
      ),
    );
  }
}

class BottomNavigationBarStyle extends BottomNavigationBarItem {
  const BottomNavigationBarStyle({required Widget icon, required String label})
      : super(icon: icon, label: label);
}
