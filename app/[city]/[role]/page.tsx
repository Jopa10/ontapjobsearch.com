import { slices } from "../../../data/getSlice"
import { notFound } from "next/navigation"

type PageProps = {
  params: {
    city: string
    role: string
  }
}

export default function Page({ params }: PageProps) {
  const key = `${params.city}/${params.role}`
  const slice = slices[key]

  if (!slice) return notFound()

  return (
    <main>
      <h1>{slice.role} jobs in {slice.city}</h1>

      {slice.jobs.map((job: any, i: number) => (
        <div key={i}>
          <h2>{job.title}</h2>
          <p>{job.company} — {job.location}</p>
          <p>{job.salary}</p>
          <a href={job.applyUrl}>Apply</a>
        </div>
      ))}
    </main>
  )
}

