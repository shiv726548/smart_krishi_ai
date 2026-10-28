import 'package:flutter/material.dart';
import '../services/api_service.dart';

class AuthScreen extends StatefulWidget {
  final VoidCallback onLoginSuccess;
  const AuthScreen({Key? key, required this.onLoginSuccess}) : super(key: key);

  @override
  _AuthScreenState createState() => _AuthScreenState();
}

class _AuthScreenState extends State<AuthScreen> {
  bool isRegister = false;
  bool _isSubmitting = false;
  String? _errorMessage;
  final _phoneController = TextEditingController();
  final _passController = TextEditingController();
  final _nameController = TextEditingController();
  String selectedLanguage = "en";

  Future<void> _submit() async {
    if (_isSubmitting) return;
    setState(() {
      _isSubmitting = true;
      _errorMessage = null;
    });
    try {
      await ApiService.authenticate(
        register: isRegister,
        phoneNumber: _phoneController.text,
        password: _passController.text,
        fullName: _nameController.text,
        language: selectedLanguage,
      );
      if (mounted) widget.onLoginSuccess();
    } catch (error) {
      if (mounted) {
        setState(() {
          _errorMessage = error.toString().replaceFirst('Exception: ', '');
        });
      }
    } finally {
      if (mounted) setState(() => _isSubmitting = false);
    }
  }

  @override
  void dispose() {
    _phoneController.dispose();
    _passController.dispose();
    _nameController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.green.shade700.withOpacity(0.2),
                  shape: BoxShape.circle,
                  border: Border.all(color: Colors.green.shade400, width: 2),
                ),
                child: const Icon(Icons.eco, size: 60, color: Colors.greenAccent),
              ),
              const SizedBox(height: 16),
              const Text(
                "Smart Krishi AI",
                style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.white),
              ),
              const SizedBox(height: 6),
              Text(
                "Smart AI & IoT Agriculture Assistant",
                style: TextStyle(fontSize: 14, color: Colors.green.shade200),
              ),
              const SizedBox(height: 32),
              Container(
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: const Color(0xFF1E293B),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: Colors.white10),
                ),
                child: Column(
                  children: [
                    Text(
                      isRegister ? "Create Farmer Account" : "Farmer Login",
                      style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white),
                    ),
                    const SizedBox(height: 20),
                    if (isRegister) ...[
                      TextField(
                        controller: _nameController,
                        style: const TextStyle(color: Colors.white),
                        decoration: const InputDecoration(
                          labelText: "Full Name",
                          labelStyle: TextStyle(color: Colors.white70),
                          prefixIcon: Icon(Icons.person, color: Colors.greenAccent),
                        ),
                      ),
                      const SizedBox(height: 12),
                    ],
                    TextField(
                      controller: _phoneController,
                      style: const TextStyle(color: Colors.white),
                      keyboardType: TextInputType.phone,
                      decoration: const InputDecoration(
                        labelText: "Phone Number",
                        labelStyle: TextStyle(color: Colors.white70),
                        prefixIcon: Icon(Icons.phone, color: Colors.greenAccent),
                      ),
                    ),
                    const SizedBox(height: 12),
                    TextField(
                      controller: _passController,
                      obscureText: true,
                      style: const TextStyle(color: Colors.white),
                      decoration: const InputDecoration(
                        labelText: "Password",
                        labelStyle: TextStyle(color: Colors.white70),
                        prefixIcon: Icon(Icons.lock, color: Colors.greenAccent),
                      ),
                    ),
                    const SizedBox(height: 20),
                    DropdownButtonFormField<String>(
                      value: selectedLanguage,
                      dropdownColor: const Color(0xFF1E293B),
                      style: const TextStyle(color: Colors.white),
                      decoration: const InputDecoration(
                        labelText: "Preferred Language",
                        labelStyle: TextStyle(color: Colors.white70),
                        prefixIcon: Icon(Icons.language, color: Colors.greenAccent),
                      ),
                      items: const [
                        DropdownMenuItem(value: "en", child: Text("English")),
                        DropdownMenuItem(value: "hi", child: Text("हिंदी (Hindi)")),
                        DropdownMenuItem(value: "mr", child: Text("मराठी (Marathi)")),
                      ],
                      onChanged: (val) => setState(() => selectedLanguage = val!),
                    ),
                    if (_errorMessage != null) ...[
                      const SizedBox(height: 8),
                      Align(
                        alignment: Alignment.centerLeft,
                        child: Text(
                          _errorMessage!,
                          style: const TextStyle(color: Colors.redAccent),
                        ),
                      ),
                    ],
                    const SizedBox(height: 24),
                    SizedBox(
                      width: double.infinity,
                      height: 50,
                      child: ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.green.shade600,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                        ),
                        onPressed: _isSubmitting ? null : _submit,
                        child: _isSubmitting
                            ? const SizedBox(
                                width: 22,
                                height: 22,
                                child: CircularProgressIndicator(
                                  strokeWidth: 2,
                                  color: Colors.white,
                                ),
                              )
                            : Text(
                                isRegister ? "Register & Continue" : "Login to Farm Dashboard",
                                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white),
                              ),
                      ),
                    ),
                    const SizedBox(height: 12),
                    TextButton(
                      onPressed: _isSubmitting
                          ? null
                          : () => setState(() {
                                isRegister = !isRegister;
                                _errorMessage = null;
                              }),
                      child: Text(
                        isRegister ? "Already registered? Login" : "New Farmer? Create Account",
                        style: const TextStyle(color: Colors.greenAccent),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
