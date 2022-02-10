import demistomock as demisto  # noqa: F401
from CommonServerPython import *  # noqa: F401
import shutil

class Client(BaseClient):
    def __init__(self, server_url, verify, proxy, headers, auth):
        super().__init__(base_url=server_url, verify=verify, proxy=proxy, headers=headers, auth=auth)

    def add_subject_request(self, subject_name):
        data = {"subject": subject_name}
        response = self._http_request('POST', 'api/v1/recognition/subjects', json_data=data)
        return response

    def rename_a_subject_request(self, old_subject_name, new_subject_name):
        data = {"subject": new_subject_name}
        response = self._http_request(
            'PUT', f'api/v1/recognition/subjects/{old_subject_name}', json_data=data)
        return response

    def list_subjects_request(self):
        response = self._http_request('GET', 'api/v1/recognition/subjects')
        return response

    def delete_subject_request(self, subject_name):
        response = self._http_request('DELETE', f'api/v1/recognition/subjects/{subject_name}',resp_type="blob")
        return response

    def delete_all_subjects_request(self):
        response = self._http_request('DELETE', 'api/v1/recognition/subjects')
        return response

    def add_an_example_of_a_subject_request(self, subject_name, image_file, det_prob_threshold=None):
        if det_prob_threshold:
            params = assign_params(subject=subject_name, det_prob_threshold=det_prob_threshold)
        else:
            params = assign_params(subject=subject_name)
        #response = self._http_request('POST', 'api/v1/recognition/faces', data={}, params=params,
                                      #files={"file": image_file})
        headers = self._headers
        headers['x-api-key'] = '3d4565d4-b1c6-42dd-b510-f4ab40939c36'

        response = requests.post(url="http://ec2-18-184-3-100.eu-central-1.compute.amazonaws.com:9000/api/v1/recognition/faces"
                                 ,verify=False, params={"subject":"test90"}, files={"file": open(image_file,'rb')}, data={})
        print(response)
        return response

    def base64_add_an_example_of_a_subject_request(self, subject, det_prob_threshold, file):
        params = assign_params(subject=subject, det_prob_threshold=det_prob_threshold)
        data = {"file": file}
        headers = self._headers
        headers['Content-Type'] = 'application/json'
        headers['x-api-key'] = '{{recognition_api_key}}'

        response = self._http_request('POST', 'api/v1/recognition/faces',
                                      params=params, json_data=data, headers=headers)

        return response

    def list_of_all_saved_examples_of_the_subject_request(self, page, size, subject):
        params = assign_params(page=page, size=size, subject=subject)
        headers = self._headers
        headers['x-api-key'] = '{{recognition_api_key}}'

        response = self._http_request('GET', 'api/v1/recognition/faces', params=params, headers=headers)

        return response

    def delete_all_examples_of_the_subject_by_name_request(self, subject):
        params = assign_params(subject=subject)
        headers = self._headers
        headers['x-api-key'] = '{{recognition_api_key}}'

        response = self._http_request('DELETE', 'api/v1/recognition/faces', params=params, headers=headers)

        return response

    def delete_an_example_of_the_subject_by_id_request(self, image_id):
        headers = self._headers
        headers['x-api-key'] = '{{recognition_api_key}}'

        response = self._http_request('DELETE', f'api/v1/recognition/faces/{image_id}', headers=headers)

        return response

    def delete_multiple_examples_request(self):
        data = {}
        headers = self._headers
        headers['x-api-key'] = '{{recognition_api_key}}'

        response = self._http_request('POST', 'api/v1/recognition/faces/delete', json_data=data, headers=headers)

        return response

    def direct_download_an_image_example_of_the_subject_by_id_request(self, recognition_api_key, image_id):
        headers = self._headers

        response = self._http_request('GET', f'api/v1/static/{recognition_api_key}/images/{image_id}', headers=headers)

        return response

    def download_an_image_example_of_the_subject_by_id_request(self, image_id):
        headers = self._headers
        headers['x-api-key'] = '{{recognition_api_key}}'

        response = self._http_request('GET', f'api/v1/recognition/faces/{image_id}/img', headers=headers)

        return response

    def recognize_faces_from_a_given_image_request(self, limit, det_prob_threshold, prediction_count, face_plugins,
                                                   status):
        params = assign_params(limit=limit, det_prob_threshold=det_prob_threshold,
                               prediction_count=prediction_count, face_plugins=face_plugins, status=status)
        headers = self._headers
        headers['Content-Type'] = 'multipart/form-data'
        headers['x-api-key'] = '{{recognition_api_key}}'

        response = self._http_request('POST', 'api/v1/recognition/recognize', params=params, headers=headers)

        return response

    def base64_recognize_faces_from_a_given_image_request(self, limit, det_prob_threshold, prediction_count,
                                                          face_plugins, status, file):
        params = assign_params(limit=limit, det_prob_threshold=det_prob_threshold,
                               prediction_count=prediction_count, face_plugins=face_plugins, status=status)
        data = {"file": file}
        headers = self._headers
        headers['Content-Type'] = 'application/json'
        headers['x-api-key'] = '{{recognition_api_key}}'

        response = self._http_request('POST', 'api/v1/recognition/recognize',
                                      params=params, json_data=data, headers=headers)

        return response

    def verify_faces_from_a_given_image_request(self, image_id, limit, det_prob_threshold, face_plugins, status):
        params = assign_params(limit=limit, det_prob_threshold=det_prob_threshold,
                               face_plugins=face_plugins, status=status)
        headers = self._headers
        headers['x-api-key'] = '{{recognition_api_key}}'

        response = self._http_request(
            'POST', f'api/v1/recognition/faces/{image_id}/verify', params=params, headers=headers)

        return response

    def base64_verify_faces_from_a_given_image_request(self, image_id, limit, det_prob_threshold, face_plugins, status,
                                                       file):
        params = assign_params(limit=limit, det_prob_threshold=det_prob_threshold,
                               face_plugins=face_plugins, status=status)
        data = {"file": file}
        headers = self._headers
        headers['Content-Type'] = 'application/json'
        headers['x-api-key'] = '{{recognition_api_key}}'

        response = self._http_request(
            'POST', f'api/v1/recognition/faces/{image_id}/verify', params=params, json_data=data, headers=headers)

        return response

    def face_detection_service_request(self, limit, det_prob_threshold, face_plugins, status):
        params = assign_params(limit=limit, det_prob_threshold=det_prob_threshold,
                               face_plugins=face_plugins, status=status)
        headers = self._headers
        headers['Content-Type'] = 'multipart/form-data'
        headers['x-api-key'] = '{{detection_api_key}}'

        response = self._http_request('POST', 'api/v1/detection/detect', params=params, headers=headers)

        return response

    def face_detection_service_base_request(self, limit, det_prob_threshold, face_plugins, status, file):
        params = assign_params(limit=limit, det_prob_threshold=det_prob_threshold,
                               face_plugins=face_plugins, status=status)
        data = {"file": file}
        headers = self._headers
        headers['Content-Type'] = 'application/json'
        headers['x-api-key'] = '{{detection_api_key}}'

        response = self._http_request('POST', 'api/v1/detection/detect', params=params, json_data=data, headers=headers)

        return response

    def face_verification_service_request(self, limit, det_prob_threshold, face_plugins, status):
        params = assign_params(limit=limit, det_prob_threshold=det_prob_threshold,
                               face_plugins=face_plugins, status=status)
        headers = self._headers
        headers['Content-Type'] = 'multipart/form-data'
        headers['x-api-key'] = '{{verification_api_key}}'

        response = self._http_request('POST', 'api/v1/verification/verify', params=params, headers=headers)

        return response

    def face_verification_service_base_request(self, limit, det_prob_threshold, face_plugins, status, source_image,
                                               target_image):
        params = assign_params(limit=limit, det_prob_threshold=det_prob_threshold,
                               face_plugins=face_plugins, status=status)
        data = {"source_image": source_image, "target_image": target_image}
        headers = self._headers
        headers['Content-Type'] = 'application/json'
        headers['x-api-key'] = '{{verification_api_key}}'

        response = self._http_request('POST', 'api/v1/verification/verify',
                                      params=params, json_data=data, headers=headers)

        return response


def add_subject_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    subject_name = args.get('subject_name')
    response = client.add_subject_request(subject_name)
    subjects_dict = {
        "name": response.get('subject')
    }
    command_results = CommandResults(
        outputs_prefix='CompreFace.Subjects',
        outputs_key_field='name',
        outputs=subjects_dict,
        raw_response=response
    )

    return command_results


def rename_subject_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    old_subject_name = args.get('old_subject_name')
    new_subject_name = args.get('new_subject_name')
    response = client.rename_a_subject_request(old_subject_name, new_subject_name)
    subjects_dict = {
        "name": old_subject_name,
        "updated": response.get('updated'),
        "new_name": new_subject_name
    }
    command_results = CommandResults(
        outputs_prefix='CompreFace.Subjects',
        outputs_key_field='name',
        outputs=subjects_dict,
        raw_response=response
    )
    return command_results


def list_subjects_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    response = client.list_subjects_request()
    subjects_dict = []
    if response.get('subjects'):
        for subject in response.get('subjects'):
            subjects_dict.append({"name": subject})
        command_results = CommandResults(
            outputs_prefix='CompreFace.Subjects',
            outputs_key_field='name',
            outputs=subjects_dict,
            raw_response=response
        )
        return command_results
    else:
        command_results = CommandResults(
            readable_output='No subjects found.'
        )
        return command_results


def delete_subject_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    subject_name = args.get('subject_name')
    client.delete_subject_request(subject_name)
    subjects_dict = {
        "name": subject_name,
        "deleted": "true"
    }
    command_results = CommandResults(
        outputs_prefix='CompreFace.Subjects',
        outputs_key_field='name',
        outputs=subjects_dict
    )
    return command_results


def delete_all_subjects_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    response = client.delete_all_subjects_request()
    command_results = CommandResults(
        readable_output=f"{response.get('deleted')} subjects deleted."
    )
    return command_results


def add_example_of_subject_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    subject_name = args.get('subject_name')
    subject_image_entryid = args.get('subject_image')
    det_prob_threshold = args.get('det_prob_threshold')
    subject_image_path = demisto.getFilePath(subject_image_entryid)['path']
    subject_image_name = demisto.getFilePath(subject_image_entryid)['name']
    print("test")
    response = client.add_an_example_of_a_subject_request(
        subject_name=subject_name,
        image_file=subject_image_path,
        det_prob_threshold=det_prob_threshold)

    subjects_dict = {
        "name": subject_name,
        "image_id": response.get('image_id')
    }
    command_results = CommandResults(
        outputs_prefix='CompreFace.Subjects',
        outputs_key_field='name',
        outputs=subjects_dict,
        raw_response=response
    )
    return command_results


def base64_add_example_of_subject_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    subject = args.get('subject')
    det_prob_threshold = args.get('det_prob_threshold')
    file = args.get('file')

    response = client.base64_add_an_example_of_a_subject_request(subject, det_prob_threshold, file)
    command_results = CommandResults(
        outputs_prefix='CompreFace.Base64AddAnExampleOfASubject',
        outputs_key_field='',
        outputs=response,
        raw_response=response
    )

    return command_results


def list_of_all_saved_examples_of_the_subject_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    page = args.get('page')
    size = args.get('size')
    subject = args.get('subject')

    response = client.list_of_all_saved_examples_of_the_subject_request(page, size, subject)
    command_results = CommandResults(
        outputs_prefix='CompreFace.ListOfAllSavedExamplesOfTheSubject',
        outputs_key_field='',
        outputs=response,
        raw_response=response
    )

    return command_results


def delete_all_examples_of_the_subject_by_name_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    subject = args.get('subject')

    response = client.delete_all_examples_of_the_subject_by_name_request(subject)
    command_results = CommandResults(
        outputs_prefix='CompreFace.DeleteAllExamplesOfTheSubjectByName',
        outputs_key_field='',
        outputs=response,
        raw_response=response
    )

    return command_results


def delete_example_of_the_subject_by_id_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    image_id = args.get('image_id')

    response = client.delete_an_example_of_the_subject_by_id_request(image_id)
    command_results = CommandResults(
        outputs_prefix='CompreFace.DeleteAnExampleOfTheSubjectById',
        outputs_key_field='',
        outputs=response,
        raw_response=response
    )

    return command_results


def delete_multiple_examples_command(client: Client, args: Dict[str, Any]) -> CommandResults:

    response = client.delete_multiple_examples_request()
    command_results = CommandResults(
        outputs_prefix='CompreFace.DeleteMultipleExamples',
        outputs_key_field='',
        outputs=response,
        raw_response=response
    )

    return command_results


def direct_download_image_example_of_the_subject_by_id_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    recognition_api_key = args.get('recognition_api_key')
    image_id = args.get('image_id')

    response = client.direct_download_an_image_example_of_the_subject_by_id_request(recognition_api_key, image_id)
    command_results = CommandResults(
        outputs_prefix='CompreFace.DirectDownloadAnImageExampleOfTheSubjectById',
        outputs_key_field='',
        outputs=response,
        raw_response=response
    )

    return command_results


def download_image_example_of_the_subject_by_id_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    image_id = args.get('image_id')

    response = client.download_an_image_example_of_the_subject_by_id_request(image_id)
    command_results = CommandResults(
        outputs_prefix='CompreFace.DownloadAnImageExampleOfTheSubjectById',
        outputs_key_field='',
        outputs=response,
        raw_response=response
    )

    return command_results


def recognize_faces_from_given_image_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    limit = args.get('limit')
    det_prob_threshold = args.get('det_prob_threshold')
    prediction_count = args.get('prediction_count')
    face_plugins = args.get('face_plugins')
    status = args.get('status')

    response = client.recognize_faces_from_a_given_image_request(limit, det_prob_threshold, prediction_count,
                                                                 face_plugins, status)
    command_results = CommandResults(
        outputs_prefix='CompreFace.RecognizeFacesFromAGivenImage',
        outputs_key_field='',
        outputs=response,
        raw_response=response
    )

    return command_results


def base64_recognize_faces_from_given_image_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    limit = args.get('limit')
    det_prob_threshold = args.get('det_prob_threshold')
    prediction_count = args.get('prediction_count')
    face_plugins = args.get('face_plugins')
    status = args.get('status')
    file = args.get('file')

    response = client.base64_recognize_faces_from_a_given_image_request(limit, det_prob_threshold, prediction_count,
                                                                        face_plugins, status, file)
    command_results = CommandResults(
        outputs_prefix='CompreFace.Base64RecognizeFacesFromAGivenImage',
        outputs_key_field='',
        outputs=response,
        raw_response=response
    )

    return command_results


def verify_faces_from_given_image_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    image_id = args.get('image_id')
    limit = args.get('limit')
    det_prob_threshold = args.get('det_prob_threshold')
    face_plugins = args.get('face_plugins')
    status = args.get('status')

    response = client.verify_faces_from_a_given_image_request(image_id, limit, det_prob_threshold, face_plugins, status)
    command_results = CommandResults(
        outputs_prefix='CompreFace.VerifyFacesFromAGivenImage',
        outputs_key_field='',
        outputs=response,
        raw_response=response
    )

    return command_results


def base64_verify_faces_from_given_image_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    image_id = args.get('image_id')
    limit = args.get('limit')
    det_prob_threshold = args.get('det_prob_threshold')
    face_plugins = args.get('face_plugins')
    status = args.get('status')
    file = args.get('file')

    response = client.base64_verify_faces_from_a_given_image_request(image_id, limit, det_prob_threshold, face_plugins,
                                                                     status, file)
    command_results = CommandResults(
        outputs_prefix='CompreFace.Base64VerifyFacesFromAGivenImage',
        outputs_key_field='',
        outputs=response,
        raw_response=response
    )

    return command_results


def face_detection_service_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    limit = args.get('limit')
    det_prob_threshold = args.get('det_prob_threshold')
    face_plugins = args.get('face_plugins')
    status = args.get('status')

    response = client.face_detection_service_request(limit, det_prob_threshold, face_plugins, status)
    command_results = CommandResults(
        outputs_prefix='CompreFace.FaceDetectionService',
        outputs_key_field='',
        outputs=response,
        raw_response=response
    )

    return command_results


def face_detection_service_base_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    limit = args.get('limit')
    det_prob_threshold = args.get('det_prob_threshold')
    face_plugins = args.get('face_plugins')
    status = args.get('status')
    file = args.get('file')

    response = client.face_detection_service_base_request(limit, det_prob_threshold, face_plugins, status, file)
    command_results = CommandResults(
        outputs_prefix='CompreFace.FaceDetectionServiceBase64',
        outputs_key_field='',
        outputs=response,
        raw_response=response
    )

    return command_results


def face_verification_service_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    limit = args.get('limit')
    det_prob_threshold = args.get('det_prob_threshold')
    face_plugins = args.get('face_plugins')
    status = args.get('status')

    response = client.face_verification_service_request(limit, det_prob_threshold, face_plugins, status)
    command_results = CommandResults(
        outputs_prefix='CompreFace.FaceVerificationService',
        outputs_key_field='',
        outputs=response,
        raw_response=response
    )

    return command_results


def face_verification_service_base_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    limit = args.get('limit')
    det_prob_threshold = args.get('det_prob_threshold')
    face_plugins = args.get('face_plugins')
    status = args.get('status')
    source_image = args.get('source_image')
    target_image = args.get('target_image')

    response = client.face_verification_service_base_request(limit, det_prob_threshold, face_plugins, status,
                                                             source_image, target_image)
    command_results = CommandResults(
        outputs_prefix='CompreFace.FaceVerificationServiceBase64',
        outputs_key_field='',
        outputs=response,
        raw_response=response
    )

    return command_results


def test_module(client: Client) -> None:
    client.list_subjects_request()
    return_results('ok')


def main() -> None:

    params: Dict[str, Any] = demisto.params()
    args: Dict[str, Any] = demisto.args()
    url = params.get('url')
    api_key = params.get('apikey')
    verify_certificate: bool = not params.get('insecure', False)
    proxy = params.get('proxy', False)

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    command = demisto.command()
    demisto.debug(f'Command being called is {command}')

    try:
        requests.packages.urllib3.disable_warnings()
        client: Client = Client(urljoin(url, ''), verify_certificate, proxy, headers=headers, auth={})

        commands = {
            'compreface-add-subject': add_subject_command,
            'compreface-rename-subject': rename_subject_command,
            'compreface-list-subjects': list_subjects_command,
            'compreface-delete-subject': delete_subject_command,
            'compreface-delete-all-subjects': delete_all_subjects_command,
            'compreface-add-example-of-subject': add_example_of_subject_command,
            'compreface-base64-add-example-of-subject': base64_add_example_of_subject_command,
            'compreface-list-of-all-saved-examples-of-the-subject': list_of_all_saved_examples_of_the_subject_command,
            'compreface-delete-all-examples-of-the-subject-by-name': delete_all_examples_of_the_subject_by_name_command,
            'compreface-delete-example-of-the-subject-by-id': delete_example_of_the_subject_by_id_command,
            'compreface-delete-multiple-examples': delete_multiple_examples_command,
            'compreface-direct-download-image-example-of-the-subject-by-id':
                direct_download_image_example_of_the_subject_by_id_command,
            'compreface-download-image-example-of-the-subject-by-id':
                download_image_example_of_the_subject_by_id_command,
            'compreface-recognize-faces-from-given-image': recognize_faces_from_given_image_command,
            'compreface-base64-recognize-faces-from-given-image': base64_recognize_faces_from_given_image_command,
            'compreface-verify-faces-from-given-image': verify_faces_from_given_image_command,
            'compreface-base64-verify-faces-from-given-image': base64_verify_faces_from_given_image_command,
            'compreface-face-detection-service': face_detection_service_command,
            'compreface-face-detection-service-base': face_detection_service_base_command,
            'compreface-face-verification-service': face_verification_service_command,
            'compreface-face-verification-service-base': face_verification_service_base_command,
        }

        if command == 'test-module':
            test_module(client)
        elif command in commands:
            return_results(commands[command](client, args))
        else:
            raise NotImplementedError(f'{command} command is not implemented.')

    except Exception as e:
        return_error(str(e))


if __name__ in ['__main__', 'builtin', 'builtins']:
    main()
