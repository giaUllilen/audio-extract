from src.service.audio_extract import AudioExtractService
import pytz
from src.utils.logger import logger

'''
 * Interseguro JOB
 * audio-extract
 * audios SAC
 *
 * @author Gianella 
'''

def main():
    audio_service = AudioExtractService()
    audio_service.execute()
    

if __name__ == "__main__":
    main()
