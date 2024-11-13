import { Outlet, useLoaderData } from "react-router-dom";
import { getData } from "../dataConnecter";

export async function loader(){
  const data = await getData();
  return { data }
}

export default function Root(){
  const data = useLoaderData();
  console.log(data);

  return (
    <div>
      Hello!
      <Outlet />
    </div>
  )
}