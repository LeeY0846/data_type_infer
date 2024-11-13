import { redirect } from "react-router-dom";
import { deleteFile } from "../dataConnecter";

export async function action({ params }:{ params: any}){
  await deleteFile(params.fileID);
  return redirect("/");
}
