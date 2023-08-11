# Selenium_start
import os
import shutil
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

# Antirobo:
# import os
import urllib
import pydub
import speech_recognition as sr
import sys
import requests
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import os
import shutil
from io import BytesIO
from zipfile import ZipFile
import requests
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from pathlib import Path


def create_folder_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def remove_rust_mozprofile_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.startswith("rust_mozprofile"):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                raise Exception(f"Error while deleting {file_path}: {e}")


def get_latest_geckodriver_version():
    response = requests.get(
        "https://api.github.com/repos/mozilla/geckodriver/releases/latest"
    )
    return response.json()["name"]


def download_and_extract_geckodriver(config_path, latest_version):
    geckodriver_url = f"https://github.com/mozilla/geckodriver/releases/download/v{latest_version}/geckodriver-v{latest_version}-win64.zip"
    response = requests.get(geckodriver_url)
    zipfile = ZipFile(BytesIO(response.content))
    zipfile.extractall(path=config_path)


def set_firefox_preferences(options, downloadfolder_path=None):
    if downloadfolder_path is not None:
        options.set_preference("browser.download.dir", downloadfolder_path)
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
    # Define additional preferences for the Firefox profile
    options.set_preference("print.always_print_silent", True)
    options.set_preference("print.printer_Microsoft_Print_to_PDF.print_command", "")
    options.set_preference(
        "print.printer_Microsoft_Print_to_PDF.printerName", "Microsoft Print to PDF"
    )
    options.set_preference("print.printer_Microsoft_Print_to_PDF.print_to_file", True)
    options.set_preference(
        "print.printer_Microsoft_Print_to_PDF.print_to_filename",
        f"{Path.home()}/Rpa_Python/Certificados_Akad/output.pdf",
    )
    options.set_preference("print.printer_Microsoft_Print_to_PDF.print_bgcolor", False)
    options.set_preference("print.show_print_progress", False)


def selenium_start(
    config_path: str, downloadfolder_path: str = None, headless: bool = True
):
    """
    Function to initialize the Selenium WebDriver for Firefox.

    Args:
        config_path (str): Local path where the geckodriver.exe file will be stored.
        downloadfolder_path (str, optional): Local path where files downloaded by Selenium will be stored. Can be set to None to skip this action.
        headless (bool): Argument to determine whether the program will run in headless mode (without a visual interface) or not.

    Returns:
        obj: webdriver.Firefox object.
    """
    create_folder_if_not_exists(config_path)
    remove_rust_mozprofile_files(downloadfolder_path)

    latest_geckodriver_version = get_latest_geckodriver_version()
    gecko_exe = f"{config_path}/geckodriver.exe"
    if not os.path.exists(gecko_exe):
        download_and_extract_geckodriver(config_path, latest_geckodriver_version)

    options = Options()
    options.headless = headless
    options.page_load_strategy = "normal"
    set_firefox_preferences(options, downloadfolder_path)

    return webdriver.Firefox(options=options, service=Service(executable_path=gecko_exe))


# Example usage:
# driver = selenium_start(config_path="/path/to/geckodriver_folder", downloadfolder_path="/path/to/download_folder", headless=True)
# driver.get("https://www.example.com")



def antirobo(driver: webdriver) -> None:
    """
    Função para escapar do sistema de recaptcha utilizando o áudio e convertendo em string.

    Args:
        driver: o webdriver do selenium.
    """

    def get_audio_by_link():
        driver.switch_to.window(driver.window_handles[1])
        sleep(0.4)
        driver.switch_to.window(driver.window_handles[0])
        sleep(0.4)
        driver.switch_to.window(driver.window_handles[1])

        src = driver.current_url
        resposta = requests.get(src)
        if resposta.status_code != 404:
            print(f"[INFO]: Link do audio: {src}")
            path_to_mp3 = os.path.normpath(
                os.path.join(os.getcwd(), f"sample{src[-1:-10]}.mp3")
            )
            path_to_wav = os.path.normpath(
                os.path.join(os.getcwd(), f"sample{src[-1:-10]}.wav")
            )
            urllib.request.urlretrieve(src, path_to_mp3)
            try:
                sound = pydub.AudioSegment.from_mp3(path_to_mp3)
                sound.export(path_to_wav, format="wav")
                sample_audio = sr.AudioFile(path_to_wav)
                print("[INFO]: Conversão mp3>wav concluida . pydub")
            except Exception:
                print("Ocorreu um erro relacionado com o . ffmpeg")
                sys.exit("[ERR] error ffmpeg")
            r = sr.Recognizer()
            with sample_audio as source:
                audio = r.record(source)
            print("[INFO]: Convertendo wav>keys . SpeechRecognition")
            try:
                key = r.recognize_google(audio, language="pt-BR")
            except:
                print("error while generating the key")
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                return 404
            os.remove(os.getcwd() + f"\\sample{src[-1:-10]}.mp3")
            os.remove(os.getcwd() + f"\\sample{src[-1:-10]}.wav")
            print(f"[INFO] Chave Recaptcha: {key}")
            print(f"[INFO]: Chave recaptcha gerada: {key}")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            return key
        else:
            print("404 notfound")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            return 404

    def get_recaptcha_frame():
        frames = driver.find_elements(By.TAG_NAME, "iframe")
        target_frames = []

        for frame in frames:
            title = frame.get_attribute("title")
            if title == "o desafio reCAPTCHA expira em dois minutos":
                # print(frames.index(frame))
                target_frames.append(frame)
            # print(title)

        if target_frames:
            for frame in target_frames:
                if frame.is_displayed():
                    # print(target_frames.index(frame))
                    # print('o frame certo é o:',frame.get_attribute("name"))
                    return frame

    def main_antirobo():
        print(driver.current_url)
        target_frame = get_recaptcha_frame()
        print(target_frame.get_attribute("name"))
        driver.switch_to.frame(target_frame)
        driver.find_element(By.ID, "recaptcha-audio-button").click()
        try:
            if driver.find_element(By.CLASS_NAME, "rc-doscaptcha-header-text"):
                raise Exception(
                    "Error while tryng to solve the recaptcha, cause: 'Seu computador ou sua rede podem estar enviando consultas automáticas.'"
                )
        except:
            pass
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "rc-audiochallenge-tdownload-link")
            )
        )
        driver.find_element(By.CLASS_NAME, "rc-audiochallenge-tdownload-link").click()
        chave_gerada = get_audio_by_link()
        if chave_gerada != 404:
            driver.switch_to.frame(target_frame)
            print(chave_gerada)
            driver.find_element(By.ID, "audio-response").send_keys(chave_gerada)
            driver.find_element(By.ID, "recaptcha-verify-button").click()
            sleep(4)
            print("clicked")
            del chave_gerada
            del target_frame
            try:
                print("pass")
            except:
                # close all tabs except for the first one
                handles = driver.window_handles
                for handle in handles[1:]:
                    driver.switch_to.window(handle)
                    driver.close()

                # switch back to the first tab
                driver.switch_to.window(handles[0])

                # navigate to a blank page
                driver.get("about:blank")
                raise Exception("error")
        else:
            print("error 404, and generation error solution:")
            # close all tabs except for the first one
            handles = driver.window_handles
            for handle in handles[1:]:
                driver.switch_to.window(handle)
                driver.close()

            # switch back to the first tab
            driver.switch_to.window(handles[0])

            # navigate to a blank page
            driver.get("about:blank")
            raise Exception("error")

    try:
        target_frame = ""
        main_antirobo()
        print("success")
    except Exception as e:
        print(e)
        # close all tabs except for the first one
        handles = driver.window_handles
        for handle in handles[1:]:
            driver.switch_to.window(handle)
            driver.close()

        # switch back to the first tab
        driver.switch_to.window(handles[0])

        # navigate to a blank page
        driver.get("about:blank")
        raise Exception("error")
