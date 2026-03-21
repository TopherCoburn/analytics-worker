// parser.js

import { parse } from 'csv-parse';
import { createReadStream } from 'fs';
import { promisify } from 'util';
import { v2 as ansiEscapes } from 'ansi-escapes';

const rl = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout,
    crlfDelay: Infinity
});

const fs = require('fs/promises');

const parseCSV = async (filePath) => {
    const readStream = createReadStream(filePath);
    const parser = parse({
        skip_lines: 1, // ignore the header row
        trim: true,
        columns: true,
        cast: (value, context) => {
            if (context.field === 'DateTime') {
                return new Date(value);
            }
            return value;
        }
    });

    const parsedData = await new Promise((resolve, reject) => {
        const rows = [];
        parser.on('readable', () => {
            let row;
            while ((row = parser.read()) !== null) {
                rows.push(row);
            }
            parser.on('end', () => resolve(rows));
        });
        parser.on('error', (err) => reject(err));
    });

    return parsedData;
};

const processLineByLine = (filePath) => {
    let lineNumber = 0;
    const processLine = (line) => {
        lineNumber++;
        console.log(`Processing line ${lineNumber}: ${ansiEscapes.red(line)}`);
        // your code here to process the line
    };

    const readStream = createReadStream(filePath);
    readStream.on('line', processLine);
    readStream.on('error', (err) => {
        console.error(`Error reading file: ${err}`);
    });
    readStream.on('end', () => {
        console.log(`Done processing file. Total lines: ${lineNumber}`);
    });
};

const processCSV = async (filePath) => {
    try {
        const data = await parseCSV(filePath);
        for (const row of data) {
            processLineByLine(JSON.stringify(row));
        }
    } catch (err) {
        console.error(`Error parsing CSV: ${err}`);
    }
};

const execute = async () => {
    const filePath = process.argv[2];
    await processCSV(filePath);
};

execute();