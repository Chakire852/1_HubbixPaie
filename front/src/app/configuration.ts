import { Injectable } from '@angular/core';

@Injectable()

// Provides configurate to composer rest Server
export class Configuration {

    public ApiIP: string = "http://127.0.0.1";
    public ApiPort: string = "8001";

    public GetAllDocuments: string =  "api/documents/all/";
    public GetArticlesByDoc: string =  "api/articles/";
    public GetArticle: string =  "api/documents/all/";
    //public GetAllArticles: string = "api/documents/all/";
    public CheckDocumentById: string = "api/documents/";
    public DeleteDocument: string = "api/documents/";
    public DeleteArticles: string = "api/articles/";
    public DownloadCode: string = "api/documents/downloadCode/"
    public SaveDocument: string = 'api/documents/';
    public SaveArticles: string = 'api/articles/';
    public SendNlp: string = 'api/documents/';
}
