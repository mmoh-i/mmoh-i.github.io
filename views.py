from flask import Blueprint,  render_template, request, flash, url_for
import pickle

views = Blueprint('views', __name__)
model = pickle.load(open('fraud_detective/model.pkl', 'rb'))

@views.route('/home')
@views.route('/')
def home():
    #logo_image = os.path.join(app.config['UPLOAD_FOLDER'], 'spy.jpg')
    return render_template("index.html")
@views.route('/predict', methods=['POST'])
def preds():
    pred_text = request.form.get("pred_txt")
    prediction_model = model.predict(pred_text)

    if prediction_model == 0:
        prediction_model = "message not-scam"
        flash('{}'.format(prediction_model), category='success')
    else:
        prediction_model = "scam message"
        flash('{}'.format(prediction_model),category='error')

if __name__ == "__main__":
    app.run(debug=True)