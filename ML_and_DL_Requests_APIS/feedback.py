from App import *

@app.route('/detection_feedback', methods=['POST'])
def feedback():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        feedback_data={}
        if data['type'] == 'crop_suggestion':
            feedback_data={
                "type": data['type'],
                "is_correct": data['is_correct'],
                "is_wrong_or_correct_reason": data['is_wrong_or_correct_reason'],
                "current_prediction":data['current_prediction']
            }
        else:
            feedback_data={
                "type": data['type'],
                "is_correct": data['is_correct'],
                "what_should_correct": data['what_should_correct'],
                "is_wrong_or_correct_reason": data['is_wrong_or_correct_reason'],
                "current_prediction":data['current_prediction']
            }
        feedbacks.insert_one(feedback_data)
        return jsonify({
            "response": "success"
        }),200
    else:
        return jsonify({"response":"Request not allowed"}),403