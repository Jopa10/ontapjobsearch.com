import { slices } from "@/data/getSlice"

export default function Page({
  params,
}: {
  params: { city: string; role: string }
}) {
  const key = `${params.city}/${params.role}`
  const slice = slices[key]

  if (!slice) return <div>Not found</div>

  const job = slice.jobs[0]

  return (
    <main style={{ padding: 40 }}>
      <h1>
        {slice.role} jobs in {slice.city}
      </h1>

      <h2>{job.title}</h2>
      <p>{job.company}</p>
      <p>{job.location}</p>
      <p>{job.salary}</p>
    </main>
  )
}


