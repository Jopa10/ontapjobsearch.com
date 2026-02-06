import { slices } from "@/data/getSlice"

export default function Page({
  params,
}: {
  params: { city: string; role: string }
}) {
  const city = decodeURIComponent(params.city).toLowerCase()
  const role = decodeURIComponent(params.role).toLowerCase()
  const key = `${city}/${role}`

  const slice = (slices as Record<string, any>)[key]

  if (!slice) {
    return (
      <div style={{ padding: 40 }}>
        <b>Not found</b>
        <div>Looking for key: {key}</div>
      </div>
    )
  }

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






