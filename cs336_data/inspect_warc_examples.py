from pathlib import Path

from fastwarc.warc import ArchiveIterator, WarcRecordType
import gzip

from cs336_data.raw_data_converter import RawDataConverter


with (
    gzip.open(Path('/mnt/c/Users/eugencutic/source/repos/assignment4-data/local-shared-data/CC/example.warc.gz'), 'rb') as f_warc,
    gzip.open(Path('/mnt/c/Users/eugencutic/source/repos/assignment4-data/local-shared-data/CC/example.warc.wet.gz'), 'rb') as f_wet,       
):
    warc_iter = ArchiveIterator(f_warc)
    wet_iter = ArchiveIterator(f_wet)

    for i, (warc_record, wet_record) in enumerate(zip(warc_iter, wet_iter)):
        if (warc_record.record_type == WarcRecordType(4)
            and warc_record.http_content_type == 'text/html'
        ):
            print(warc_record.headers.get('WARC-Target-URI'))
            body = warc_record.reader.read()
            converted_body = RawDataConverter.extract_text(body)
            wet_content = wet_record.reader.read()

            example_warc_path = Path(f'./local-shared-data/CC/example_warc_content_{i}')
            example_warc_converted_content_path = Path(f'./local-shared-data/CC/example_warc_converted_content_{i}')
            example_wet_path = Path(f'./local-shared-data/CC/example_wet_content_{i}')

            uri = str(warc_record.headers.get('WARC-Target-URI', '')) + '\n\n'

            with open(example_warc_path, 'wb') as f_out:    
                f_out.write(uri.encode('utf-8'))
                f_out.write(body)

            with open(example_warc_converted_content_path, 'wb') as f_out:    
                f_out.write(uri.encode('utf-8'))
                f_out.write(converted_body.encode('utf-8'))

            with open(example_wet_path, 'wb') as f_out:    
                f_out.write(uri.encode('utf-8'))
                f_out.write(wet_content)

        if i == 3:
            break

