from time import sleep
import requests

def dummy_task(file_path, poll_interval=5, max_attempts=5):
    base_url = r'http://127.0.0.1:8000'
    predict_task_url = base_url + '/predict'
    with open(file_path, 'rb') as file:
        task = requests.post(predict_task_url, files={'file': file})
    task_id = task.json()['task_id']
    predict_result_url = base_url + '/result/' + task_id
    attempts = 0
    result = None
    while attempts < max_attempts:
        attempts += 1
        result_response = requests.get(predict_result_url)
        if result_response.status_code == 200:
            result = result_response.json()['predicted_class']
            break
        sleep(poll_interval)
    return result


if __name__ == '__main__':
    file_path = 'test_imgs/mnist_3.jpeg'
    prediction = dummy_task(file_path)
    print(prediction)
