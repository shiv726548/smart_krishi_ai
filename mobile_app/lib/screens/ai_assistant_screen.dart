import 'package:flutter/material.dart';
import '../services/api_service.dart';

class AIAssistantScreen extends StatefulWidget {
  const AIAssistantScreen({Key? key}) : super(key: key);

  @override
  _AIAssistantScreenState createState() => _AIAssistantScreenState();
}

class _AIAssistantScreenState extends State<AIAssistantScreen> {
  final TextEditingController _controller = TextEditingController();
  final List<Map<String, String>> _messages = [
    {
      "sender": "bot",
      "text": "I am a rule-based demo assistant, not an agricultural diagnosis service. Ask for general information and verify crop-specific decisions locally."
    }
  ];
  String currentLang = "en";
  bool isThinking = false;

  void _sendMessage() async {
    final text = _controller.text.trim();
    if (text.isEmpty) return;

    setState(() {
      _messages.add({"sender": "user", "text": text});
      _controller.clear();
      isThinking = true;
    });

    final reply = await ApiService.askAiAssistant(text, currentLang);

    if (mounted) {
      setState(() {
        isThinking = false;
        _messages.add({"sender": "bot", "text": reply});
      });
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E293B),
        title: Row(
          children: const [
            Icon(Icons.psychology, color: Colors.cyanAccent),
            SizedBox(width: 8),
            Text("Rule-based Farming Demo", style: TextStyle(color: Colors.white, fontSize: 18)),
          ],
        ),
        actions: [
          DropdownButton<String>(
            value: currentLang,
            dropdownColor: const Color(0xFF1E293B),
            underline: const SizedBox(),
            icon: const Icon(Icons.language, color: Colors.greenAccent),
            items: const [
              DropdownMenuItem(value: "en", child: Text("EN", style: TextStyle(color: Colors.white))),
              DropdownMenuItem(value: "hi", child: Text("HI", style: TextStyle(color: Colors.white))),
              DropdownMenuItem(value: "mr", child: Text("MR", style: TextStyle(color: Colors.white))),
            ],
            onChanged: (val) => setState(() => currentLang = val!),
          ),
          const SizedBox(width: 12),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, idx) {
                final msg = _messages[idx];
                final isUser = msg["sender"] == "user";
                return Align(
                  alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.only(bottom: 12),
                    padding: const EdgeInsets.all(14),
                    constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.8),
                    decoration: BoxDecoration(
                      color: isUser ? Colors.green.shade700 : const Color(0xFF1E293B),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: isUser ? Colors.greenAccent : Colors.white10),
                    ),
                    child: Text(
                      msg["text"]!,
                      style: const TextStyle(color: Colors.white, fontSize: 14),
                    ),
                  ),
                );
              },
            ),
          ),
          if (isThinking)
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  SizedBox(width: 16, height: 16, child: CircularProgressIndicator(color: Colors.cyanAccent, strokeWidth: 2)),
                  SizedBox(width: 8),
                  Text("Preparing a rule-based reply...", style: TextStyle(color: Colors.cyanAccent, fontSize: 12)),
                ],
              ),
            ),

          // Voice & Text Input Toolbar
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            color: const Color(0xFF1E293B),
            child: Row(
              children: [
                const IconButton(
                  tooltip: "Voice input is not configured; type a question",
                  icon: Icon(Icons.mic_off, color: Colors.white38),
                  onPressed: null,
                ),
                Expanded(
                  child: TextField(
                    controller: _controller,
                    style: const TextStyle(color: Colors.white),
                    decoration: const InputDecoration(
                      hintText: "Ask a general farming question...",
                      hintStyle: TextStyle(color: Colors.white38),
                      border: InputBorder.none,
                    ),
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.send, color: Colors.greenAccent),
                  onPressed: _sendMessage,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
